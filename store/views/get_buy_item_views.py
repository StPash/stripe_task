from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.conf import settings
import stripe

from store.models.item import Item


def get_item_view(request, item_id):
    # item = Item.objects.filter(id=item_id).first()
    item = get_object_or_404(Item, id=item_id)
    return render(request, 'store/item.html', {
        'item': item,
        'stripe_key': settings.STRIPE_KEYS[item.currency]['public_key'],
        'domain': request.build_absolute_uri('/')[:-1]
    })


def buy_item_view(request, item_id):
    # item = Item.objects.filter(id=item_id).first()
    item = get_object_or_404(Item, id=item_id)
    stripe.api_key = settings.STRIPE_KEYS[item.currency]['secret_key']
    domain = request.build_absolute_uri('/')[:-1]
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price_data': {
                        'currency': item.currency,
                        'product_data': {'name': item.name},
                        'unit_amount': int(item.price * 100),
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=domain + f'/success/',
            cancel_url=domain + f'/cancel/',
        )
    except Exception as e:
        return str(e)
    print(checkout_session.id)
    return JsonResponse({'id': checkout_session.id})
