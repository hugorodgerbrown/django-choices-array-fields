import pytest
from django import forms
from django.core.exceptions import ValidationError

from choices_fields.fields import IntegerChoicesArrayField, TextChoicesArrayField
from demo.models import CustomUser


@pytest.mark.django_db
def test_user_type() -> None:
    user = CustomUser.objects.create(username="foo")
    assert user.user_type == []
    user.user_type.append(CustomUser.UserType.OWNER)
    assert user.user_type == ["owner"]
    user.user_type.append(CustomUser.UserType.ADMIN)
    assert user.user_type == ["owner", "admin"]
    user.save()
    user.refresh_from_db()
    assert user.user_type == ["owner", "admin"]


@pytest.mark.django_db
def test_user_status() -> None:
    user = CustomUser.objects.create(username="foo")
    assert user.user_status == []
    user.user_type.append(CustomUser.UserStatus.ONE)
    assert user.user_type == [1]
    user.user_type.append(CustomUser.UserStatus.TWO)
    assert user.user_type == [1, 2]
    user.save()
    user.refresh_from_db()
    assert user.user_type == [1, 2]


class TestTextChoicesArrayField:
    def test_formfield_defaults(self) -> None:
        field = TextChoicesArrayField(choices=CustomUser.UserType.choices)
        formfield = field.formfield()
        assert isinstance(formfield, forms.TypedMultipleChoiceField)
        assert formfield.choices == CustomUser.UserType.choices
        assert formfield.coerce == str
        assert formfield.empty_value == ""


class TestIntegerChoicesArrayField:
    def test_formfield_defaults(self) -> None:
        field = IntegerChoicesArrayField(choices=CustomUser.UserType.choices)
        formfield = field.formfield()
        assert isinstance(formfield, forms.TypedMultipleChoiceField)
        assert formfield.choices == CustomUser.UserType.choices
        assert formfield.coerce == int
        assert formfield.empty_value is None

    def test_formfield_validate(self) -> None:
        field = IntegerChoicesArrayField(choices=CustomUser.UserStatus.choices)
        field.validate([1], None)
        field.validate([1,2], None)
        field.validate([1,2,3], None)

    def test_formfield_validate__error(self) -> None:
        field = IntegerChoicesArrayField(choices=CustomUser.UserStatus.choices)
        with pytest.raises(ValidationError) as exc_info:
            field.validate([1,2,3,4], None)
        assert exc_info.value.code == "invalid_choice"
        assert exc_info.value.params["value"] == 4
