import pytest
from typing import List

from django.urls import reverse

from src.article import Board

from .conftest import VALID_BOARD_DATA


@pytest.mark.django_db
class TestBoardCreationSuccess:
    def test_correct_http_response(self, create_boards, user):
        """GIVEN valid board data and an authenticated user

        WHEN that user tries to create the board

        THEN a 201 status code and the correct board data
        with additional meta information is returned.
        """
        response = create_boards(num_boards=1, data=VALID_BOARD_DATA)
        print(response.json())
        assert response.status_code == 201

        response_body = response.json()

        # Expected to return board data with some extra information
        expected_response_data = VALID_BOARD_DATA.copy()
        expected_response_data.update({
            'category': 'PCB',
            'owner': user.email
        })

        # Expected response data is subset of actual response
        assert expected_response_data.items() <= response_body.items()

    def test_board_inserted_into_db(
            self,
            create_boards,
    ):
        """GIVEN valid board data and an authenticated user

        WHEN that user tries to create the board

        THEN the board is inserted into the database.
        """
        response = create_boards(num_boards=1, data=VALID_BOARD_DATA)
        board_id = response.json()["id"]
        assert Board.objects.filter(id=board_id, **VALID_BOARD_DATA).exists()


@pytest.mark.django_db
class TestBoardCreationFailure:
    def test_correct_http_response_for_anonymous_user(self, create_boards):
        """GIVEN valid board data and an anonymous user

        WHEN that user tries to create the board

        THEN a 403 status code and a rejection message is returned.
        """
        response = create_boards(anonymous=True)
        assert response.status_code == 403

        response_body = response.json()
        expected_response_body = {
            "detail": "Authentication credentials were not provided."
        }
        assert response_body == expected_response_body

    def test_board_not_created_for_anonymous_user(self, create_boards):
        """GIVEN valid board data and an anonymous user

        WHEN that user tries to create the board

        THEN the board is not inserted into the database.
        """
        create_boards(anonymous=True)
        assert not Board.objects.filter(**VALID_BOARD_DATA).exists()

    @pytest.mark.xfail
    @pytest.mark.parametrize("missing_attribute", [attribute for attribute in VALID_BOARD_DATA["attributes"]])
    def test_correct_http_response_to_incomplete_board(self, missing_attribute, create_boards):
        """GIVEN incomplete board data and an authenticated user

        WHEN that user tries to create the board

        THEN a 400 status code and the correct error message are returned.
        """
        incomplete_data = VALID_BOARD_DATA.copy()
        del incomplete_data["attributes"][missing_attribute]

        response = create_boards(data=incomplete_data, num_boards=1)
        assert response.status_code == 400

        response_body = response.json()
        expected_response_body = {
            missing_attribute: [
                "This field is required."
            ]
        }
        assert response_body == expected_response_body

    @pytest.mark.xfail
    @pytest.mark.parametrize("missing_attribute", [attribute for attribute in VALID_BOARD_DATA])
    def test_incomplete_board_not_inserted_into_db(self, missing_attribute, create_boards):
        """GIVEN incomplete board data and an authenticated user

        WHEN that user tries to create the board

        THEN the board is not inserted into the database.
        """
        incomplete_data = VALID_BOARD_DATA.copy()
        del incomplete_data["attributes"][missing_attribute]

        create_boards(data=incomplete_data, num_boards=1)

        assert not Board.objects.filter(**incomplete_data).exists()


@pytest.mark.django_db
class TestBoardList:
    def test_200_status_and_list_is_complete(self, create_boards, authenticated_client):
        """GIVEN an authenticated user who has created some boards

        WHEN that user requests a list of their boards (GET)

        THEN all of the created boards are present, and the HTTP
        response contains the complete information for all boards.
        The user is listed as board owner.
        """
        NUM_BOARDS = 3
        create_boards(num_boards=NUM_BOARDS)

        response = authenticated_client.get(path=reverse("shop:board_list"))
        assert response.status_code == 200

        board_list = response.json()
        assert len(board_list) == NUM_BOARDS

    def test_boards_in_list_have_correct_owner(self, create_boards, user, authenticated_client):
        """GIVEN an authenticated user who has created some boards

        WHEN that user requests a list of their boards (GET)

        THEN the user is listed as board owner in all of them and
        each one contains the correct information.
        """
        create_boards(num_boards=3)

        response = authenticated_client.get(path=reverse("shop:board_list"))
        board_list = response.json()
        for board in board_list:
            assert board["owner"] == user.email

            # Data used to create the board is contained in the response body
            assert VALID_BOARD_DATA.items() <= board.items()

    def test_board_list_does_not_contain_other_users_boards(self, create_boards, client, other_user):
        """GIVEN an authenticated user who has created some boards

        WHEN a different user requests a list of their own boards (GET)

        THEN none of the former user's boards are present in the HTTP
        response - instead, the response contains an empty list.
        """
        # One user creates a board.
        create_boards(num_boards=1)

        # A different user who has not created boards yet requests a list of her boards.
        client.logout()
        client.force_login(other_user)
        response = client.get(path=reverse("shop:board_list"))

        board_list = response.json()
        assert isinstance(board_list, List)
        assert len(board_list) == 0


@pytest.mark.django_db
class TestBoardDetailsSuccess:
    """Collection of test cases for retrieving board details."""
    def test_get_details_for_owned_board(self, authenticated_client, user, create_boards):
        """GIVEN an authenticated user who has created a board

        WHEN they request details of that board (GET)

        THEN those details are returned together with
        a 200 status code, listing the user as board owner.
        """
        post_response = create_boards(data=VALID_BOARD_DATA, num_boards=1)
        board_id = post_response.json()["id"]

        get_response = authenticated_client.get(path=reverse("shop:board_details", args=[board_id]))
        board_details = get_response.json()

        assert get_response.status_code == 200
        assert board_details["owner"] == user.email

        # Data used to create the board is contained in the response body
        assert VALID_BOARD_DATA.items() <= board_details.items()


@pytest.mark.django_db
class TestBoardDetailsFailure:
    def test_no_details_for_other_users_board(self, authenticated_client, create_boards, other_user):
        """GIVEN an authenticated user who has created a board

        WHEN a different user requests details of that board (GET)

        THEN permission is rejected together with a 403
        status code.
        """
        # One user creates a board
        post_response = create_boards(num_boards=1)
        board_id = post_response.json()["id"]

        # A different user requests details about that board
        authenticated_client.logout()
        authenticated_client.force_login(other_user)

        get_response = authenticated_client.get(path=reverse("shop:board_details", args=[board_id]))
        assert get_response.status_code == 403

        response_body = get_response.json()
        assert response_body.get("detail") == "You do not have permission to perform this action."

    def test_get_404_for_non_exiting_board(self, authenticated_client):
        """GIVEN an authenticated user

        WHEN they request details of a board that does not exist (GET)

        THEN a 404 response is received.
        """
        NON_EXISTING_BOARD_ID = 9999
        path = reverse("shop:board_details", args=[NON_EXISTING_BOARD_ID])
        response = authenticated_client.get(path=path)

        assert response.status_code == 404
