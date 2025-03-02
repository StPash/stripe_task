from django.db import models
from django.urls import reverse

from store.models.discount import Discount
from store.models.item import Item
from store.models.tax import Tax


class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='order_items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(default=1,  verbose_name="Количество")

    def __str__(self):
        return f"{self.quantity} x {self.item.name}"

    class Meta:
        verbose_name = "Товар в заказе"
        verbose_name_plural = "Товары в заказе"


class Order(models.Model):
    items = models.ManyToManyField(Item, through='OrderItem')
    tax = models.ForeignKey(Tax, on_delete=models.SET_NULL, blank=True,  null=True, verbose_name="Налог")
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, blank=True,  null=True, verbose_name="Скидка")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f'Order id: {self.pk}'

    def get_absolute_url(self):
        return reverse('get_order', args=[self.pk])
