from .models import Category
from .cart import Cart


def menu_categories(request):
    categories = Category.objects.all()

    return {'menu_categories':categories}


def cart(request):
    return {'cart': Cart(request)}


