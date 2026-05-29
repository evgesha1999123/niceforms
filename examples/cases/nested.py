"""Пример вложенных моделей (nested forms).

Что происходит:

User содержит:
Address
Coordinates
Appearance
Всё это автоматически превращается в вложенную форму

Что полезного показывает:

Как niceforms строит иерархию форм
Работа с Optional вложенными объектами"""

from typing import Optional

from nicegui import APIRouter, ui
from pydantic import BaseModel, Field

from ._layout import base, TheNavigation
from niceforms import BaseModelForm

router = APIRouter()


class Coordinates(BaseModel):
    x: float
    y: float


class Address(BaseModel):
    """Address"""

    street: str
    city: str
    coordinates: Coordinates


class Person(BaseModel):
    """Some description"""

    name: str
    age: int


class Relationship(BaseModel):
    users: list[Person]


class Appearance(BaseModel):
    """Appearance"""

    hair: str
    height: int


class User(Person):
    """Some description"""

    address: Optional[Address]
    appearance: Appearance = Field(
        ..., title="Внешний вид", description="Отличительные черты персоны"
    )
    relationship: Relationship = Field(
        title="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
        description='Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem.',
    )


@router.page('/nested')
@base
async def nested() -> None:

    with ui.column().classes('w-full max-w-2xl mx-auto'):
        TheNavigation(description='Когда структура данных сложная и вложенная').render()

        async def submit_handler(model: User) -> None:
            print(f"Пользователь создан: {model.model_dump()}")

        form = BaseModelForm[User](
            User,
            on_submit=submit_handler,
        )
        del form.buttons['json']
        del form.buttons['submit']
        form.render()
