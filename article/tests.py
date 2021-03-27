import pytest
from typing import Callable, List, Optional, Dict

from django.test import Client
from django.urls import reverse

from user.models import User
from article.models import Board, ArticleCategory


@pytest.fixture
def user_factory(db) -> Callable:
    """Returns a closure that can be called to
    create a standard user."""
    def create_user(
        email: str = "user@gmail.com",
        password: str = "pcb_password",
        username: str = "example_user",
        first_name: Optional[str] = "Max",
        last_name: Optional[str] = "Mustermann",
        is_staff: str = False,
        is_superuser: str = False,
        is_active: str = True
    ) -> User:
        user = User.objects.create_user(
            password=password,
            first_name=first_name,
            username=username,
            last_name=last_name,
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=is_active,
        )
        return user
    return create_user


@pytest.fixture
def user(user_factory) -> User:
    return user_factory()


@pytest.fixture
def other_user(user_factory) -> User:
    return user_factory(
        email="other_user@gmail.com",
        username="other_example_user"
    )


@pytest.fixture
def authenticated_client(db, client, user) -> Client:
    """Returns standard pytest client authenticated
    with a given user.
    """
    client.force_login(user)
    return client


@pytest.fixture()
def pcb_category(db) -> None:
    """Inserts the PCB article category into the test database."""
    pcb_cat = ArticleCategory(
        articleCategoryID=1,
        name="PCB",
        description="Printed Circuit Board"
    )
    pcb_cat.save()


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


class TestBoardCreation:
    """Collection of test cases for creating PCBs."""
    @pytest.mark.django_db
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
            'id': 1,
            'owner': 'user@gmail.com'
        })
        # Expected response is subset of actual response
        assert expected_response.items() <= response.json().items()
        assert Board.objects.all().count() == 1

    @pytest.mark.django_db
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

    @pytest.mark.django_db
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


class TestBoardList:
    """Collection of test cases for retrieving board lists."""
    @pytest.mark.django_db
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

    @pytest.mark.django_db
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
