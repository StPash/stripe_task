from django.db import models
from django.urls import reverse

CURRENCIES = {
    'usd': 'USD',
    'rub': 'RUB'
}


class Item(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    currency = models.CharField(max_length=3, default='usd', choices=CURRENCIES)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return f'{self.name}: {self.price} {self.currency.upper()}'

    def get_absolute_url(self):
        return reverse('get_item', args=[self.pk])
