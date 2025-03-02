from django.db import models


class Tax(models.Model):
    amount = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Процент налога")

    class Meta:
        verbose_name = "Налог"
        verbose_name_plural = "Налоги"

    def __str__(self):
        return f'Налог {self.amount}%'
