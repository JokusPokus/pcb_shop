import pytest
from typing import Callable, List, Optional, Dict

from django.test import Client
from django.urls import reverse

from user.models import User
from article.models import Board, ArticleCategory


@pytest.fixture()
def valid_board_data() -> Dict:
    return {
        "dimensionX": 100,
        "dimensionY": 100,
        "gerberFileName": "gerber.zip",
        "gerberHash": "blablub123",
        "differentDesigns": 1,
        "layers": 3,
        "deliveryFormat": "Single PCB",
        "thickness": 1.6,
        "color": "Red",
        "surfaceFinish": "no",
        "copperWeight": 2,
        "goldFingers": "no",
        "castellatedHoles": "no",
        "removeOrderNum": "yes",
        "confirmProdFile": "yes",
        "flyingProbeTest": "no"
    }


@pytest.mark.django_db
class TestBoardCreation:
    """Collection of test cases for creating PCBs."""
    def test_create_valid_board_with_authenticated_user(
            self,
            authenticated_client,
            pcb_category,
            valid_board_data
    ):
        """GIVEN valid board data and an authenticated user

        WHEN that user tries to create the board

        THEN a 201 status code and the correct board data
        with additional meta information is returned.
        The board is inserted into the database.
        """
        response = authenticated_client.post(path=reverse("shop:board_list"), data=valid_board_data)
        assert response.status_code == 201

        # Expected to return board data with some extra information
        expected_response = valid_board_data.copy()
        expected_response.update({
            'category': 'PCB',
            'owner': 'user@gmail.com'
        })
        # Expected response is subset of actual response
        assert expected_response.items() <= response.json().items()
        assert Board.objects.all().count() == 1

    def test_reject_creating_valid_board_with_anonymous_user(
            self,
            client,
            pcb_category,
            valid_board_data
    ):
        """GIVEN valid board data and an anonymous user

        WHEN that user tries to create the board

        THEN a 403 status code and a rejection message is returned.
        The board is not inserted into the database.
        """
        response = client.post(path=reverse("shop:board_list"), data=valid_board_data)
        assert response.status_code == 403

        expected_response = {
            "detail": "Authentication credentials were not provided."
        }
        assert response.json() == expected_response
        assert not Board.objects.all().exists()

    def test_reject_creating_incomplete_board(
            self,
            authenticated_client,
            pcb_category,
            valid_board_data
    ):
        """GIVEN incomplete board data and an authenticated user

        WHEN that user tries to create the board

        THEN a 400 status code and an appropriate error message is returned.
        The board is not inserted into the database.
        """
        def create_board_without(attr: str):
            """Sends POST request to create a board where the :attr:
            information is missing and returns the response.
            """
            board_data = valid_board_data.copy()
            del board_data[attr]
            res = authenticated_client.post(path=reverse("shop:board_list"), data=board_data)
            return res

        for attribute in valid_board_data:
            response = create_board_without(attribute)
            assert response.status_code == 400

            expected_response = {
                attribute: [
                    "This field is required."
                ]
            }
            assert response.json() == expected_response
            assert not Board.objects.all().exists()


@pytest.mark.django_db
class TestBoardList:
    """Collection of test cases for retrieving board lists."""
    def test_get_list_of_owned_boards(
            self,
            authenticated_client,
            pcb_category,
            valid_board_data
    ):
        """GIVEN an authenticated user who has created some boards

        WHEN that user requests a list of their boards (GET)

        THEN all of the created boards are present, and the HTTP
        response contains the complete information for all boards.
        The user is listed as board owner.
        """
        for _ in range(3):
            authenticated_client.post(path=reverse("shop:board_list"), data=valid_board_data)

        response = authenticated_client.get(path=reverse("shop:board_list"))
        assert response.status_code == 200

        board_list = response.json()
        assert len(board_list) == 3

        for board in board_list:
            assert board["owner"] == "user@gmail.com"

            # Data used to create the board is contained in the response body
            assert valid_board_data.items() <= board.items()

    def test_board_list_does_not_contain_other_users_boards(
            self,
            authenticated_client,
            other_user,
            pcb_category,
            valid_board_data
    ):
        """GIVEN an authenticated user who has created some boards

        WHEN a different user requests a list of their own boards (GET)

        THEN none of the former user's boards are present in the HTTP
        response - instead, the response contains an empty list.
        """
        # One user creates a board
        authenticated_client.post(path=reverse("shop:board_list"), data=valid_board_data)

        # A different user requests a list of their boards
        authenticated_client.logout()
        authenticated_client.force_login(other_user)
        response = authenticated_client.get(path=reverse("shop:board_list"))

        assert isinstance(response.json(), List)
        assert len(response.json()) == 0


@pytest.mark.django_db
class TestBoardDetails:
    """Collection of test cases for retrieving board details."""
    def test_get_details_for_owned_board(
            self,
            authenticated_client,
            pcb_category,
            valid_board_data
    ):
        """GIVEN an authenticated user who has created a board

        WHEN they request details of that board (GET)

        THEN those details are returned together with
        a 200 status code, listing the user as board owner.
        """
        post_response = authenticated_client.post(path=reverse("shop:board_list"), data=valid_board_data)
        board_id = post_response.json()["id"]

        get_response = authenticated_client.get(path=reverse("shop:board_details", args=[board_id]))
        board_details = get_response.json()

        assert get_response.status_code == 200
        assert board_details["owner"] == "user@gmail.com"

        # Data used to create the board is contained in the response body
        assert valid_board_data.items() <= board_details.items()

    def test_not_get_details_for_other_users_board(
            self,
            authenticated_client,
            other_user,
            pcb_category,
            valid_board_data
    ):
        """GIVEN an authenticated user who has created a board

        WHEN a different user requests details of that board (GET)

        THEN permission is rejected together with a 403
        status code.
        """
        # One user creates a board
        post_response = authenticated_client.post(path=reverse("shop:board_list"), data=valid_board_data)
        board_id = post_response.json()["id"]

        # A different user requests details about that board
        authenticated_client.logout()
        authenticated_client.force_login(other_user)
        get_response = authenticated_client.get(path=reverse("shop:board_details", args=[board_id]))

        assert get_response.status_code == 403
        assert get_response.json().get("detail") == "You do not have permission to perform this action."

    def test_get_404_for_non_exiting_board(
            self,
            authenticated_client,
    ):
        """GIVEN an authenticated user

        WHEN they request details of a board that does not exist (GET)

        THEN a 404 response is received.
        """
        response = authenticated_client.get(path=reverse("shop:board_details", args=[1]))

        assert response.status_code == 404
