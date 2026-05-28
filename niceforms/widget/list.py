import json
from typing import List, Optional, Union

from nicegui import ui
from nicegui.elements.mixins.validation_element import ValidationElement

from niceforms import BaseValidationWidget
from niceforms.utils import normalize_type


class ListWidget(BaseValidationWidget):
    type_tip_map: dict[type, str] = {
        List[str]: '["яблоко", "банан", "апельсин"]',
        List[int]: '[423, 324, 983]',
        list[str]: '["яблоко", "банан", "апельсин"]',
        list[int]: '[423, 324, 983]',
    }

    def collect(self) -> Optional[Union[list, tuple]]:
        if self.element.value is not None:
            try:
                return json.loads(self.element.value)
            except json.decoder.JSONDecodeError:
                return None

        return None

    def render(self) -> ValidationElement:
        if self.default_value is None:
            default_value = None

        elif isinstance(self.default_value, str):
            # строку не сериализуем повторно
            default_value = self.default_value

        else:
            # dict/list/int/bool/etc -> JSON строка
            default_value = json.dumps(
                self.default_value,
                ensure_ascii=False,
                indent=2,
            )

        def decode_validate(v) -> bool:
            if not v:
                return True

            try:
                json.loads(v)
            except (
                    json.decoder.JSONDecodeError,
                    TypeError,
            ):
                return False

            return True

        validation = {
            **self.default_validations,
            'Не валидный JSON': lambda v: decode_validate(v),
        }

        el = (
            ui.textarea(
                value=default_value,
                placeholder=self.placeholder,
                validation=validation,
            )
            .props("outlined dense")
            .classes("w-full font-mono")
        )

        # Контейнер для лейбла и иконки
        with ui.row().classes('items-center gap-1'):
            ui.label(
                text='Строка парсится как JSON'
            ).classes('text-xs mt-1')

            normalized_type = normalize_type(self.field.annotation)

            example = self.type_tip_map.get(normalized_type.origin_type)

            if example is not None:
                ui.icon(
                    'info',
                    size='xs',
                ).classes(
                    'cursor-help mt-1'
                ).tooltip(
                    f'Пример ввода: {example}'
                ).style(
                    'color: #8989ff'
                )

        return el
