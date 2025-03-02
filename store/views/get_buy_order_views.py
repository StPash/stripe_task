from django.http import JsonResponse, Http404
from django.shortcuts import render
from django.conf import settings
from django.db.models import Prefetch
import stripe

from store.models.order import Order, OrderItem


def get_order_view(request, order_id):
    order = Order.objects.select_related('tax', 'discount').prefetch_related(
        Prefetch('order_items',
                 queryset=OrderItem.objects.select_related('item'),
                 to_attr='prefetch_order_items'
                 )).filter(id=order_id).first()
    if order is None:
        raise Http404("Order not found")

    return render(request, 'store/order.html', {
        'order': order,
        'stripe_key': settings.STRIPE_KEYS[order.prefetch_order_items[0].item.currency]['public_key'],
        'domain': request.build_absolute_uri('/')[:-1]
    })


def buy_order_view(request, order_id):
    order = Order.objects.select_related('tax', 'discount').prefetch_related(
        Prefetch('order_items',
                 queryset=OrderItem.objects.select_related('item'),
                 to_attr='prefetch_order_items'
                 )).filter(id=order_id).first()
    if order is None:
        raise Http404("Order not found")
    # валюту оплаты заказа принимаем по первому товару в заказе
    payment_currency = order.prefetch_order_items[0].item.currency

    stripe.api_key = settings.STRIPE_KEYS[payment_currency]['secret_key']
    domain = request.build_absolute_uri('/')[:-1]

    # создание объекта скидки (stripe.Coupon) при наличии скидки у заказа, получение его id
    discounts = []
    if order.discount:
        discounts.append({
            'coupon': stripe.Coupon.create(
                percent_off=order.discount.amount,
                duration='once',
            ).id
        })

    # создание объекта налога (stripe.TaxRate) при наличии налога у заказа, получение его id
    tax_rates = []
    if order.tax:
        tax_rate = stripe.TaxRate.create(
            display_name='Some Tax',
            inclusive=False,
            percentage=order.tax.amount,
        )
        tax_rates.append(tax_rate.id)

    # формирование списка товаров для создания сессии
    items = []
    for order_item in order.prefetch_order_items:
        if order_item.item.currency != payment_currency:
            return JsonResponse({'error': f'В заказе id: {order.id} присутствуют товары, цены которых представлены разными валютами.'})

        items.append(
            {
                'price_data': {
                    'currency': order_item.item.currency,
                    'product_data': {'name': order_item.item.name},
                    'unit_amount': int(order_item.item.price * 100),
                },
                'tax_rates': tax_rates,
                'quantity': order_item.quantity,
            }
        )

    try:
        # создание объекта сессии для оплаты
        checkout_session = stripe.checkout.Session.create(
            line_items=items,
            mode='payment',
            discounts=discounts,
            success_url=domain + f'/success/',
            cancel_url=domain + f'/cancel/',
        )
    except Exception as e:
        return str(e)
    print(checkout_session.id)
    return JsonResponse({'id': checkout_session.id})
