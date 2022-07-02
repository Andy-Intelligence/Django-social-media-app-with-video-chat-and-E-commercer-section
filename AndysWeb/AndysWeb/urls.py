from django import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from projectApp.views import activityPage, add_product, become_vendor, cart_detail, category, contact, createMember, deleteMember, deleteRoom, edit_vendor, frontpage, getMember, getToken, home, lobby, pollIndex, pollResult, pollVote, room, createRoom, search, success, updateRoom, deleteRoom, loginPage, logoutUser, registerPage, deleteMessage, updateUser, userprofile, topicsPage, vendor, vendor_admin, vendors, vidRoom, product
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('room/<str:pk>/', room, name='room'),
    path('create-room/', createRoom, name='create-room'),
    path('update-room/<str:pk>/', updateRoom, name='update-room'),
    path('delete-room/<str:pk>/', deleteRoom, name="delete-room"),
    path('login/', loginPage, name="login"),
    path('logout/', logoutUser, name='logout'),
    path('register/', registerPage, name='register'),
    path('delete-message/<str:pk>/', deleteMessage, name="delete-message"),
    path('profile/<str:pk>/', userprofile, name="user-profile"),
    path('update-user/', updateUser, name="update-user"),
    path('topics/', topicsPage, name="topics"),
    path('activity/', activityPage, name="activity"),
    path('api/', include('projectApp.api.urls')),
    path('vidRoom/', vidRoom, name="vidRoom"),
    path('lobby/', lobby, name="lobby"),
    path('get_token/', getToken),
    path('create_member/', createMember),
    path('get_member/', getMember),
    path('delete_member/', deleteMember),
    path('front_page/', frontpage, name="front-page"),
    path('contact/', contact, name="contact"),
    path('become_vendor/', become_vendor, name="become_vendor"),
    path('vendor_admin/', vendor_admin, name="vendor_admin"),
    path('add-product/', add_product, name='add_product'),
    path(' <slug:category_slug>/<slug:product_slug>/', product, name='product'),
    path(' <slug:category_slug>/', category, name='category'),
    path('search/', search, name='search'),
    path('cart/', cart_detail, name='cart'),
    path('success/', success, name='success'),
    path('edit-vendor/', edit_vendor, name='edit_vendor'),
    path('vendors/',vendors, name='vendors'),
    path('<int:vendor_id>/',vendor, name='vendor'),
    path('pollIndex/', pollIndex, name="pollIndex"),
    path('pollVote/<str:pk>', pollVote, name="pollVote"),
    path('pollResult/<str:pk>', pollResult, name="pollResult"),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
