import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_stripe_product(name):
    product = stripe.Product.create(name=name)
    print(product)
    return product

def create_stripe_price(unit_amount, currency, product_id):
    price = stripe.Price.create(
        unit_amount=unit_amount,
        currency=currency,
        product=product_id,
    )
    print(price)
    return price

def create_stripe_session(price_id, success_url, cancel_url):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': price_id,
            'quantity': 1,
        }],
        mode='payment',
        success_url=success_url,
        cancel_url=cancel_url,
    )
    print(session)
    return session