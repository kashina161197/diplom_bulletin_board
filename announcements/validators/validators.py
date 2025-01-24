from pathlib import Path

from rest_framework.exceptions import ValidationError

from announcements.models import Announcement


class ForbiddenWordValidator:
    """Валидатор для проверки текста на запрещенные слова"""

    __slots__ = ("announcement_title", "announcement_description", "review_text")

    def __init__(
        self, announcement_title=None, announcement_description=None, review_text=None
    ):
        self.announcement_title = announcement_title
        self.announcement_description = announcement_description
        self.review_text = review_text

    def __call__(self, value):

        announcement_title_field = value.get(self.announcement_title)
        announcement_description_field = value.get(self.announcement_description)
        review_text_field = value.get(self.review_text)

        with open(
            Path(__file__).parent.joinpath("forbidden_words.txt"), "r", encoding="utf-8"
        ) as file:
            forbidden_words = file.read().splitlines()

        for word in forbidden_words:
            try:
                if (
                    word in announcement_title_field.lower()
                    or word in announcement_description_field.lower()
                ):
                    raise ValidationError("Имеется запрещенное слово в тексте")
            except TypeError:
                pass
            except AttributeError:
                pass
            try:
                if word in review_text_field.lower():
                    raise ValidationError("Имеется запрещенное слово в тексте")
            except TypeError:
                pass
            except AttributeError:
                pass


class RepeatAnnouncementValidator(ForbiddenWordValidator):
    """Валидатор для проверки повторения объявления"""

    __slots__ = ("title", "description", "price")

    def __init__(self, title, description, price):
        super().__init__(announcement_title=title, announcement_description=description)
        self.price = price

    def __call__(self, value):
        title_field = value.get(self.announcement_title)
        description_field = value.get(self.announcement_description)
        price_field = value.get(self.price)

        if Announcement.objects.filter(
            title=title_field, description=description_field, price=price_field
        ).exists():
            raise ValidationError("Такое объявление уже существует")


def price_zero_validator(value):
    """Валидатор для проверки цены объявления равной нулю"""

    if not value:
        raise ValidationError("Цена объявления не может быть равна нулю")
