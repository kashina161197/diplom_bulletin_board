from django.db import models

from users.models import CustomsUser


class Announcement(models.Model):
    """Модель объявления"""

    title = models.CharField(
        max_length=50,
        verbose_name="Название товара",
        help_text="Укажите название товара",
    )
    price = models.PositiveIntegerField(
        verbose_name="Цена товара", help_text="Укажите стоимость товара"
    )
    description = models.TextField(null=True, blank=True, verbose_name="Описание")
    image = models.ImageField(upload_to="announcement/photo", null=True)
    owner = models.ForeignKey(
        CustomsUser,
        verbose_name="Владелец объявления",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="announcements",
    )
    created_at = models.DateField(
        auto_now_add=True, verbose_name="Дата и время создания объявления"
    )

    def __str__(self):
        return f"№ {self.pk} - {self.title}"

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ["-created_at"]


class Review(models.Model):
    """Модель отзыва"""

    text = models.TextField(
        verbose_name="Текст отзыва",
        help_text="Расскажите о товаре и о ваших впечатлениях",
    )
    owner = models.ForeignKey(
        CustomsUser,
        on_delete=models.SET_NULL,
        verbose_name="Владелец отзыва",
        blank=True,
        null=True,
        related_name="author_reviews",
    )
    announcement = models.ForeignKey(
        Announcement,
        on_delete=models.CASCADE,
        verbose_name="Объявление, под которым отзыв",
        related_name="announcement_reviews",
    )
    created_at = models.DateTimeField(
        verbose_name="Дата создания отзыва",
        auto_now_add=True,
    )
    rating = models.IntegerField(
        verbose_name="Оценка",
        help_text="Оцените объявление от 1 до 5",
        choices=[(i, str(i)) for i in range(1, 6)],
    )

    def __str__(self):
        return f"Отзыв от {self.owner}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ["-created_at"]
