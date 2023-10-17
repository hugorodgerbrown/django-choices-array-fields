from __future__ import annotations

from typing import Any

from django import forms
from django.db import models


class ChoicesArrayField(models.JSONField):
    """Custom field used to store multiple choice values."""

    default_coerce_func = str
    default_empty_value = None
    default_choices_form_class = forms.TypedMultipleChoiceField
    default_widget = forms.CheckboxSelectMultiple

    def __init__(
        self, *, choices: models.TextChoices | models.IntegerChoices, **kwargs: Any
    ) -> None:
        self.choices = choices
        self.widget = kwargs.pop("widget", self.default_widget)
        defaults = {"blank": True, "default": list, "choices": self.choices}
        defaults.update(kwargs)
        super().__init__(**defaults)

    def deconstruct(self) -> tuple[str, str, list[Any], dict[str, Any]]:
        name, path, args, kwargs = super().deconstruct()
        kwargs["choices"] = self.choices
        return name, path, args, kwargs

    def formfield(self, **kwargs: Any) -> forms.Field:
        defaults = {
            "choices_form_class": self.default_choices_form_class,
            "choices": self.choices,
            "coerce": self.default_coerce_func,
            "empty_value": self.default_empty_value,
            "widget": self.widget,
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)


class TextChoicesArrayField(ChoicesArrayField):
    """Custom field used to store multiple TextChoices values."""

    default_coerce_func = str
    default_empty_value = ""


class IntegerChoicesArrayField(ChoicesArrayField):
    """Custom field used to store multiple TextChoices values."""

    default_coerce_func = int
    default_empty_value = None
