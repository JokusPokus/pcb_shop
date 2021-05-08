import json
import pytest
from typing import List

from django.urls import reverse

from article.models import Board

from . import BoardFactory
from . import VALID_BOARD_DATA


@pytest.mark.django_db
class TestBoardCreationSuccess:
    def test_correct_http_response(self, django_db_setup, authenticated_client, user):
        """GIVEN valid board data and an authenticated user

        WHEN that user tries to create the board

        THEN a 201 status code is returned and the board is
        inserted into the database with the correct user.
        """
        board_data = VALID_BOARD_DATA.copy()
        board_data["attributes"] = json.dumps(board_data["attributes"])

        response = authenticated_client.post(path=reverse("shop:board_list"), data=board_data)
        assert response.status_code == 201

        board_id = response.json()["id"]
        assert user.boards.filter(id=board_id, **VALID_BOARD_DATA).exists()


@pytest.mark.django_db
class TestBoardCreationFailure:
    def test_anonymous_user_cannot_create_board(self, client):
        """GIVEN valid board data and an anonymous user

        WHEN that user tries to create the board

        THEN a 403 status code is returned and the board is
        not inserted into the database.
        """
        board_data = VALID_BOARD_DATA.copy()
        board_data["attributes"] = json.dumps(board_data["attributes"])

        response = client.post(path=reverse("shop:board_list"), data=board_data)
        assert response.status_code == 403

        assert not Board.objects.filter(**VALID_BOARD_DATA).exists()

    @pytest.mark.skip
    @pytest.mark.parametrize("missing_attribute", [attribute for attribute in VALID_BOARD_DATA["attributes"]])
    def test_incomplete_board_is_not_created(self, missing_attribute, create_boards):
        """GIVEN incomplete board data and an authenticated user

        WHEN that user tries to create the board

        THEN a 400 status code is returned and the board
        is not inserted into the database.
        """
        incomplete_data = VALID_BOARD_DATA.copy()
        del incomplete_data["attributes"][missing_attribute]

        response = create_boards(data=incomplete_data, num_boards=1)
        assert response.status_code == 400
        assert not Board.objects.filter(**incomplete_data).exists()


@pytest.mark.django_db
class TestBoardList:
    def test_board_list_is_complete(self, authenticated_client, user, other_user):
        """GIVEN an authenticated user who has created some boards

        WHEN that user requests a list of their boards (GET)

        THEN all of the created boards are present, but none of the
        boards not owned by the user.
        """
        owned_board_ids = set()

        NUM_OWNED_BOARDS = 3
        for _ in range(NUM_OWNED_BOARDS):
            board = BoardFactory(owner=user)
            owned_board_ids.add(board.id)

        NUM_NON_OWNED_BOARDS = 3
        for _ in range(NUM_NON_OWNED_BOARDS):
            BoardFactory(owner=other_user)

        response = authenticated_client.get(path=reverse("article:board_list"))
        assert response.status_code == 200

        # Returned boards contain owned boards but not non-owned boards
        response_body = response.json()
        returned_board_ids = {board["id"] for board in response_body}
        assert owned_board_ids == returned_board_ids


@pytest.mark.django_db
class TestBoardListFailure:
    def test_anonymous_user_cannot_get_board_list(self, client):
        """GIVEN an anonymous user

        WHEN she tries to request a list of boards

        THEN the request is rejected and the correct HTTP response is returned."""
        response = client.get(path=reverse("article:board_list"))
        assert response.status_code == 403


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
