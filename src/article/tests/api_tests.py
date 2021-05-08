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
    def test_anonymous_user_cannot_create_board(self, django_db_setup, client):
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
    def test_incomplete_board_is_not_created(self, django_db_setup, missing_attribute, authenticated_client):
        """GIVEN incomplete board data and an authenticated user

        WHEN that user tries to create the board

        THEN a 400 status code is returned and the board
        is not inserted into the database.
        """
        board_data = VALID_BOARD_DATA.copy()
        del board_data["attributes"][missing_attribute]

        response = authenticated_client.post(path=reverse("shop:board_list"), data=board_data)
        assert response.status_code == 400
        assert not Board.objects.filter(**board_data).exists()


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
    def test_get_details_for_owned_board(self, authenticated_client, user):
        """GIVEN an authenticated user with an existing board

        WHEN they request details of that board

        THEN those details are returned together with
        a 200 status code, listing the user as board owner.
        """
        board = Board.objects.create(owner=user, **VALID_BOARD_DATA)

        response = authenticated_client.get(path=reverse("shop:board_details", args=[board.id]))
        assert response.status_code == 200

        board_details = response.json()
        assert board_details["owner"] == user.email
        assert board_details["attributes"] == VALID_BOARD_DATA["attributes"]


@pytest.mark.django_db
class TestBoardDetailsFailure:
    def test_no_details_for_other_users_board(self, authenticated_client, other_user):
        """GIVEN an authenticated user

        WHEN she tries to get details for a board she does not own

        THEN permission is rejected together with a 403
        status code.
        """
        # Create board not owned by user of interest
        board = Board.objects.create(owner=other_user, **VALID_BOARD_DATA)

        # User of interest tries to access board details
        response = authenticated_client.get(path=reverse("shop:board_details", args=[board.id]))
        assert response.status_code == 403

    def test_no_details_for_non_existing_board(self, authenticated_client):
        """GIVEN an authenticated user

        WHEN he requests details of a board that does not exist

        THEN a 404 response is returned.
        """
        NON_EXISTING_BOARD_ID = 9999
        response = authenticated_client.get(path=reverse("shop:board_details", args=[NON_EXISTING_BOARD_ID]))
        assert response.status_code == 404
