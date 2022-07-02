from .cart import Cart

from .models import Order, OrderItem


def checkout(request, first_name, last_name, email, phone, address, zipcode, place, amount):
    order = Order.objects.create(first_name=first_name, last_name=last_name, email=email,
                                 phone=phone, address=address, zipcode=zipcode, place=place, paid_amount=amount)

    for item in Cart(request):
        OrderItem.objects.create(
            order=order, product=item['product'], vendor=item['product'].vendor, price=item['product'].price, quantity=item['quantity'])

        order.vendors.add(item['product'].vendor)
    return order
