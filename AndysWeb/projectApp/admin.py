from django.contrib import admin
from .models import Room, RoomMember, Topic, Message, User, Vendor, Category, Product, Order, OrderItem, Question, Choice


# Register your models here.
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(User)
admin.site.register(RoomMember)
admin.site.register(Vendor)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Question)
admin.site.register(Choice)

