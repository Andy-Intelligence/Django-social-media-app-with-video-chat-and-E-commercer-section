from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import User
from io import BytesIO
from PIL import Image
from django.core.files import File


# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True, default="avatar.svg")
    # created_at = models.DateTimeField(auto_now_add=True)
    # created_by = models.OneToOneField(
    #     User, related_name='vendor', on_delete=models.CASCADE)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    def get_balance(self):
        items = self.items.filter(vendor_paid=False, order__vendors__in=[self.id])
        return sum((item.product.price*item.quantity) for item in items)


    def get_paid_amount(self):
        items = self.items.filter(vendor_paid=False, order__vendors__in=[self.id])
        return sum((item.product.price*item.quantity) for item in items)



class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(
        User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name

    def __str__(self):
        return self.description[0:50]


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]


###################################################################################

################### DATABASE FOR vidROOM #########################################

class RoomMember(models.Model):
    name = models.CharField(max_length=200)
    uid = models.CharField(max_length=1000)
    room_name = models.CharField(max_length=200)
    insession = models.BooleanField(default=True)

    def __str__(self):
        return self.name


########################################################################


################ multi vendors E COMMERCE SECTION #####################################
class Vendor(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.OneToOneField(
        User, related_name='vendor', on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']

        def __str__(self):
            return self.name

    

class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    ordering = models.IntegerField(default=0)

    class Meta:
        ordering = ['ordering']

    def __str__(self):
        return self.title


class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name='products', on_delete=models.CASCADE)
    vendor = models.ForeignKey(
        User, related_name='products', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    date_added = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return self.title

    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url

        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return self.thumbnail.url

            else:
                return 'https://via.placeholder.com/240*180.jpg'

    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail


class Order(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_amount = models.DecimalField(max_digits=8, decimal_places=2)
    vendors = models.ManyToManyField(User, related_name='orders')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.first_name


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name='items', on_delete=models.CASCADE)
    vendor = models.ForeignKey(
        User, related_name='items', on_delete=models.CASCADE)
    vendor_paid = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return '%s' % self.id


    def get_total_price(self):
        return self.price* self.quantity


    

##############################################################################

############################### Polls App section ##################################



class Question(models.Model):
    question = models.CharField(max_length=300)

    def __str__(self):
        return self.question

class Choice(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE,related_name='choices')
    option = models.CharField(max_length=100)
    vote = models.IntegerField(default=0)


    def __str__(self):
        return self.option


