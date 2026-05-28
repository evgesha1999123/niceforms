from nicegui import APIRouter, ui, app
from pydantic import BaseModel, Field

from niceforms import BaseModelForm


class TestCase(BaseModel):
    tags: list[str]
    users: list[int]
    persons: list[int] | None
    person_ids: list[int] | None = Field(default=[])

router = APIRouter()


obj = TestCase(tags=['tests'], users=[1, 2], persons=[1, 2])

@router.page('/')
async def basic() -> None:
    with ui.column().classes('w-full max-w-xl mx-auto'):
        async def on_submit(m: BaseModel) -> None:
            print(m)


        form = BaseModelForm(TestCase, on_submit=on_submit)
        form.wrapper_classes = form.wrapper_classes + ' max-w-xl'
        form.render()

        form.fill(obj.model_dump())


app.include_router(router)

ui.run(show=False, reload=False)
