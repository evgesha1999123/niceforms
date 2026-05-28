"""Ошибка при просмотре виджета - списка у формы

При просмотре содержимого списочного виджета у формы падает ошибка
ERROR: nicegui BaseModelForm.render() got an unexpected keyword argument 'as_card'
Traceback (most recent call last):
File "/home/evgesha/PycharmProjects/med-forms/.venv/lib/python3.12/site-packages/nicegui/events.py", line 469, in handle_event
result = cast(Callable[[], Any], handler)()
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/evgesha/PycharmProjects/med-forms/.venv/lib/python3.12/site-packages/niceforms/widget/list_basemodel/component.py", line 65, in
on_click=lambda: self.on_edit(
^^^^^^^^^^^^^
File "/home/evgesha/PycharmProjects/med-forms/.venv/lib/python3.12/site-packages/niceforms/widget/list_basemodel/component.py", line 166, in show_edit_dialog
).render()
^^^^^^^^
File "/home/evgesha/PycharmProjects/med-forms/.venv/lib/python3.12/site-packages/niceforms/widget/list_basemodel/dialog.py", line 62, in render
self.form.render(as_card=False, body_classes='w-full')
TypeError: BaseModelForm.render() got an unexpected keyword argument 'as_card'
"""

from datetime import date
from typing import Optional

from nicegui import APIRouter, ui, app
from pydantic import BaseModel, Field, constr

from niceforms import BaseModelForm

router = APIRouter()


class RecipeDTO(BaseModel):
    evnrecept_id: Optional[int] = Field(None, title='ID рецепта')
    evnrecept_setdt: Optional[date] = Field(None, title='Дата выписки рецепта')
    evnrecept_num: constr(max_length=50) | None = Field(None, title='Номер рецепта')


class PatientCardDTO(BaseModel):
    recipe: list[RecipeDTO] = Field(title='Рецепты')
    name: str


@router.page('/')
def page() -> None:
    with ui.column().classes('w-full max-w-xl mx-auto'):

        form = BaseModelForm[PatientCardDTO](
            PatientCardDTO,
            title="Карточка пациента",
            view_annotation_type=False,
            view_type_error_message=False,
        )
        form.render()
        form.fill(
            {
                'recipe': [
                    RecipeDTO(
                        evnrecept_id=0, evnrecept_num='12', evnrecept_setdt=date.today()
                    ).model_dump(),
                    RecipeDTO(
                        evnrecept_id=5, evnrecept_num='13', evnrecept_setdt=date.today()
                    ).model_dump(),
                ]
            }
        )


app.include_router(router)

ui.run(show=False, reload=False)
