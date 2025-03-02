from django.contrib import admin

from store.models.item import Item
from store.models.order import Order, OrderItem
from store.models.tax import Tax
from store.models.discount import Discount

# Register your models here.
admin.site.register(Item)
admin.site.register(Tax)
admin.site.register(Discount)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ('id', 'get_items', 'tax', 'discount')

    def get_items(self, obj):
        return ", ".join([item.name for item in obj.items.all()])

    get_items.short_description = 'Товары'


# 123admin456
# admin1@el.com
# admin1