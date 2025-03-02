from django.db import models


class Discount(models.Model):
    amount = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Процент скидки")

    class Meta:
        verbose_name = "Скидка"
        verbose_name_plural = "Скидки"

    def __str__(self):
        return f'Скидка {self.amount}%'
