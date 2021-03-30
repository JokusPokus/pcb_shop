import pytest

from typing import Callable, Optional
from django.test import Client

from user.models import User
from article.models import ArticleCategory


@pytest.fixture
def user_factory() -> Callable:
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
def authenticated_client(client, user) -> Client:
    """Returns standard pytest client authenticated
    with a given user.
    """
    client.force_login(user)
    return client


@pytest.fixture()
def create_pcb_category() -> None:
    """Inserts the PCB article category into the test database."""
    pcb_cat = ArticleCategory(
        articleCategoryID=1,
        name="PCB",
        description="Printed Circuit Board"
    )
    pcb_cat.save()
