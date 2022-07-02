from itertools import product
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from projectApp.context_processors import cart
from .models import Room, Topic, Message, User, RoomMember, Vendor, Product, Category,Question,Choice
from .forms import CheckoutForm, MyUserCreationForm, RoomForm, UserForm, UserCreationForm, ProductForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from agora_token_builder import RtcTokenBuilder
from django.http import JsonResponse
import random
import time
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm
from django.utils.text import slugify
from .forms import AddToCart
from .cart import Cart
import stripe
from .utilities import checkout

from django.conf import settings


def loginPage(request):

    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)

        except:
            messages.error(request, 'User does not exist')

        user = authenticate(email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            messages.error(request, 'Username or password does not exist')

    context = {'page': page}
    return render(request, 'projectApp/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):

    form = MyUserCreationForm()
    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')

        else:
            messages.error(request, 'An error occured during registration')

    context = {'form': form}
    return render(request, 'projectApp/login_register.html', context)


def home(request):

    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(
        name__icontains=q) | Q(description__icontains=q))
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {'rooms': rooms, 'topics': topics,
               'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'projectApp/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages,
               'participants': participants}
    return render(request, 'projectApp/room.html', context)


def userprofile(request, pk):

    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms,
               'room_messages': room_messages, 'topics': topics}
    return render(request, 'projectApp/profile.html', context)


@login_required(login_url='/login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        # print(request.POST)
        # print(request.POST.get('name'))
        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host = request.user
        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'projectApp/room_form.html', context)


def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse("You are not allowed here!!")

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        form = RoomForm(request.POST, instance=room)
        room.name = request.POST.get('topic')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'room': room}

    return render(request, 'projectApp/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse("You are not allowed here")
    if request.method == "POST":
        room.delete()
        return redirect('home')

    context = {'obj': room}
    return render(request, 'projectApp/delete.html', context)


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse("You are not allowed here")
    if request.method == "POST":
        message.delete()
        return redirect('home')

    context = {'obj': message}
    return render(request, 'projectApp/delete.html', context)


@login_required(login_url='login')
def updateUser(request):

    user = request.user
    form = UserForm(instance=user)

    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    context = {'form': form}

    return render(request, 'projectApp/update-user.html', context)


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    context = {'topics': topics}
    return render(request, 'projectApp/topics.html', context)


def activityPage(request):
    room_messages = Message.objects.all()
    context = {'room_messages': room_messages}
    return render(request, 'projectApp/activity.html', context)


#################################################################################################################################

# VIDEO CHAT SIDE

#################################################################################################################################


def vidRoom(requests):
    context = {}
    return render(requests, 'projectApp/vidRoom.html', context)


def lobby(requests):
    context = {}
    return render(requests, 'projectApp/lobby.html', context)


def getToken(request):
    appId = "54ae82a3bd424b87b2af80d060820d28"
    appCertificate = "91f317d464f14206ba381e607118d529"
    channelName = request.GET.get('channel')
    uid = random.randint(1, 230)
    expirationTimeInSeconds = 3600
    currentTimeStamp = int(time.time())
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(
        appId, appCertificate, channelName, uid, role, privilegeExpiredTs)

    return JsonResponse({'token': token, 'uid': uid}, safe=False)


@csrf_exempt
def createMember(request):
    data = json.loads(request.body)
    member, created = RoomMember.objects.get_or_create(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )

    return JsonResponse({'name': data['name']}, safe=False)


def getMember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    member = RoomMember.objects.get(
        uid=uid,
        room_name=room_name,
    )
    name = member.name
    return JsonResponse({'name': member.name}, safe=False)


@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)
    member = RoomMember.objects.get(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )
    member.delete()
    return JsonResponse('Member deleted', safe=False)

###################################################################

############## E commerce ###########################################


def frontpage(request):

    newest_products = Product.objects.all()[0:8]

    context = {'newest_products': newest_products}
    return render(request, 'projectApp/frontpage.html', context)


def contact(request):

    context = {}
    return render(request, 'projectApp/contact.html', context)


def become_vendor(request):

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            login(request, user)

            vendor = Vendor.objects.create(name=user.username, created_by=user)

            return redirect('frontpage')

    else:
        form = UserCreationForm()

        context = {'form': form}
        return render(request, 'projectApp/become_vendor.html', context)


@login_required(login_url='login')
def vendor_admin(request):
    vendor = request.user  # .vendor
    products = Product.objects.all()
    orders = vendor.orders.all()

    for order in orders:
        order.vendor_amount = 0
        order.vendor_paid_amount = 0
        order.fully_paid = True

        for item in order.items.all():
            if item.vendor == request.user:     # .vendor
                

                if item.vendor_paid:
                    order.vendor_paid_amount += item.get_total_price()
                
                else:
                    order.vendor_amount += item.get_total_price()
                    order.fully_paid = False

    context = {'vendor': vendor, 'products': products, 'orders':orders}

    return render(request, 'projectApp/vendor_admin.html', context)


@login_required(login_url='login')
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = request.user  # .vendor
            product.slug = slugify(product.title)
            product.save()

            return redirect('vendor_admin')

    else:
        form = ProductForm()

    context = {'form': form}

    return render(request, 'projectApp/add_product.html', context)


def product(request, category_slug, product_slug):

    cart = Cart(request)
    product = get_object_or_404(
        Product, category__slug=category_slug, slug=product_slug)

    if request.method == 'POST':
        form = AddToCart(request.POST)

        if form.is_valid():
            quantity = form.cleaned_data['quantity']

            cart.add(product_id=product.id,
                     quantity=quantity, update_quantity=False)
            messages.success(request, 'The product was added to the cart')

            return redirect('product', category_slug=category_slug, product_slug=product_slug)

    else:
        form = AddToCart()

    similar_products = list(product.category.products.exclude(id=product.id))

    if len(similar_products) >= 4:
        similar_products = random.sample(similar_products, 4)

    context = {'product': product,
               'similar_products': similar_products, 'form': form}
    return render(request, 'projectApp/product.html', context)


def category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)

    context = {'category': category}
    return render(request, 'projectApp/category.html', context)


def search(request):
    query = request.GET.get('query') if request.GET.get(
        'query') != None else ''

    products = Product.objects.filter(Q(title__icontains=query) | Q(
        description__icontains=query))
    context = {'products': products, 'query': query}
    return render(request, 'projectApp/search.html', context)


def cart_detail(request):

    cart = Cart(request)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            stripe.api_key = settings.STRIPE_SECRET_KEY

            stripe_token = form.cleaned_data['stripe_token']

            charge = stripe.Charge.create(
                amount=int(cart.get_total_cost()*100),
                currency='USD',
                description='Charge from Interiorshop',
                source=stripe_token
            )

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            address = form.cleaned_data['address']
            zipcode = form.cleaned_data['zipcode']
            place = form.cleaned_data['place']

            order = checkout(request, first_name, last_name, email, phone,
                             address, zipcode, place,  cart.get_total_cost())

            cart.clear()

            return redirect('success')
    else:
        form = CheckoutForm()
    remove_from_cart = request.GET.get('remove_from_cart', '')

    change_quantity = request.GET.get('change_quantity', '')
    quantity = request.GET.get('quantity', 0)

    if remove_from_cart:
        cart.remove(remove_from_cart)

        return redirect('cart')

    if change_quantity:
        cart.add(change_quantity, quantity, True)

        return redirect('cart')

    context = {'form': form, 'stripe_pub_key': settings.STRIPE_PUB_KEY}
    return render(request, 'projectApp/cart.html', context)


def success(request):
    return render(request, 'projectApp/success.html')



@login_required(login_url='login')
def edit_vendor(request):
    vendor = request.user# .vendor

    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')


        if name:
            vendor.created_by_email = email
            vendor.created_by.save()

            vendor.name = name
            vendor.save()

            return redirect('vendor_admin')

    context = {'vendor':vendor}
    return render(request, 'projectApp/edit_vendor.html',context)




def vendors(request):
    vendors = User.objects.all()
    context =  {'vendors':vendors}

    return render(request, 'projectApp/vendors.html',context)


def vendor(request, vendor_id):
    vendor = get_object_or_404(User, pk=vendor_id)
    context = {'vendor': vendor}

    return render(request, 'projectApp/vendor.html', context)



#######################################################################################

########################### pollsApp Section ##############################




def pollIndex(request): 


    questions = Question.objects.all()

    context = {'questions':questions}

    return render(request, 'projectApp/pollIndex.html', context)



def pollVote(request,pk): 
    question = Question.objects.get(id=pk)
    options = question.choices.all()

    # if request.method == 'POST':
    #     inputvalue = request.POST['choice']
    #     select_option = options.get(id=inputvalue)
    #     select_option.vote += 1
    #     select_option.save()



    context = {'question':question, 'options':options}

    return render(request, 'projectApp/pollVote.html', context)



def pollResult(request,pk): 
    question = Question.objects.get(id=pk)
    options = question.choices.all()

    if request.method == 'POST':
        inputvalue = request.POST['choice']
        select_option = options.get(id=inputvalue)
        select_option.vote += 1
        select_option.save()
    context = {'question':question, 'options':options}

    return render(request, 'projectApp/pollResult.html', context)



