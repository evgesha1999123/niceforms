from typing import TypeAlias, Callable, Any

from nicegui.elements.input import Input
from nicegui.events import Handler, ValueChangeEventArguments

ValidationFunction: TypeAlias = Callable[[Any], str | None]
ValidationDict = dict[str, Callable[[Any], bool]]


class LazyErrorInput(Input):
    def __init__(
        self,
        label: str | None = None,
        *,
        placeholder: str | None = None,
        value: str = "",
        password: bool = False,
        password_toggle_button: bool = False,
        prefix: str | None = None,
        suffix: str | None = None,
        on_change: Handler[ValueChangeEventArguments] | None = None,
        autocomplete: list[str] | None = None,
    ) -> None:
        super().__init__(
            label,
            placeholder=placeholder,
            value=value,
            password=password,
            password_toggle_button=password_toggle_button,
            prefix=prefix,
            suffix=suffix,
            on_change=on_change,
            autocomplete=autocomplete,
            validation=None,
        )

    def lazy_validate(self, validator: ValidationFunction | ValidationDict) -> None:
        error = None

        if callable(validator):
            error = validator(self.value)

        elif isinstance(validator, dict):
            for error_text, rule in validator.items():
                result = rule(self.value)

                if not result:
                    error = error_text  # первая ошибка
                    break

        else:
            raise ValueError("`validator` must be a callable or a dict")

        if error:
            self.error = error
        else:
            self.error = None
