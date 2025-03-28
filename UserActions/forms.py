from django import forms
from django_select2.forms import Select2Widget

from blogs.models import User


class InputUserLogin(forms.Form):
    """
    Форма для ввода или выбора логина пользователя.

    Эта форма предназначена для отображения выпадающего списка логинов пользователей,
    с возможностью ввода логина вручную.

    Поля:
        input_login (ChoiceField): Поле для выбора или ввода логина пользователя.
            - Предоставляет список логинов, загружаемых через метод `get_user_choices`.
            - Также поддерживает возможность ввода логина вручную, если он не найден в списке.
            - Используется виджет `Select2Widget` для улучшения интерфейса выбора.
    """
    input_login = forms.ChoiceField(
        label="Логин Пользователя",
        choices=[],
        required=False,
        widget=Select2Widget(attrs={'class': 'form-select', 'data-placeholder': 'Введите или выберите логин'})
    )

    def __init__(self, *args, **kwargs) -> None:
        """
        Инициализация формы с заполнением выбора логинов.

        При инициализации формы происходит вызов метода `get_user_choices`, который заполняет
        поле выбора доступными логинами пользователей.

        Аргументы:
            *args, **kwargs: Передаются аргументы родительскому классу `forms.Form`.
        """
        super().__init__(*args, **kwargs)
        self.fields["input_login"].choices = self.get_user_choices()

    @staticmethod
    def get_user_choices() -> list[tuple[str, str]]:
        """
        Получение списка логинов всех пользователей.

        Этот метод формирует список кортежей для поля выбора логинов пользователей.
        Список логинов пользователей загружается из базы данных.

        Возвращает:
            list: Список кортежей в формате (значение, отображаемое название), включая
            опцию для ввода логина вручную.
        """
        users = User.objects.all()
        choices = [("", "--- Введите или выберите логин ---")] + [(user.login, user.login) for user in users]
        return choices


