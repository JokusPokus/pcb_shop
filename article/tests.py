import pytest
from typing import Callable, List, Optional
from django.test import Client

from user.models import User
from .models import Board, ArticleCategory


@pytest.fixture
def user_factory(db) -> Callable:
    # Closure
    def create_user(
        email: str = "hanno@gmail.com",
        password: str = "pcb_password",
        username: str = "Hanno",
        first_name: Optional[str] = "Hanno",
        last_name: Optional[str] = "vom Krähenwald",
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
def authenticated_client(db, client, user_factory) -> Client:
    user = user_factory()
    client.force_login(user)
    return client


@pytest.fixture()
def pcb_category(db) -> None:
    pcb_cat = ArticleCategory(
        articleCategoryID=1,
        name="PCB",
        description="Printed Circuit Board"
    )
    pcb_cat.save()


class TestBoardCreation:
    VALID_BOARD_DATA = {
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
    def test_create_valid_board_with_authenticated_user(self, authenticated_client, pcb_category):
        response = authenticated_client.post(path="/shop/user/boards/", data=self.VALID_BOARD_DATA)
        assert response.status_code == 201

        # Expected to return board data with some extra information
        expected_response = self.VALID_BOARD_DATA.copy()
        expected_response.update({
            'category': 'PCB',
            'id': 1,
            'owner': 'hanno@gmail.com'
        })
        # Expected response is subset of actual response
        assert expected_response.items() <= response.json().items()
        assert len(Board.objects.all()) == 1

    @pytest.mark.django_db
    def test_reject_create_valid_board_with_unauthenticated_user(self, client, pcb_category):
        response = client.post(path="/shop/user/boards/", data=self.VALID_BOARD_DATA)
        assert response.status_code == 403

        expected_response = {
            "detail": "Authentication credentials were not provided."
        }
        assert response.json() == expected_response
        assert not Board.objects.all().exists()

    @pytest.mark.django_db
    def test_reject_create_incomplete_board(self, authenticated_client, pcb_category):
        def create_board_without(attr):
            board_data = self.VALID_BOARD_DATA.copy()
            del board_data[attr]
            response = authenticated_client.post(path="/shop/user/boards/", data=board_data)
            return response

        for attribute in self.VALID_BOARD_DATA:
            response = create_board_without(attribute)
            assert response.status_code == 400

            expected_response = {
                attribute: [
                    "This field is required."
                ]
            }
            assert response.json() == expected_response
            assert not Board.objects.all().exists()
