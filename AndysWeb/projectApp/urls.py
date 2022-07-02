

from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('AndysWeb.urls')),
    # path('vendors/', include('AndysWeb.urls')),

    # path('api/', include('projectApp.api.urls')), this is meant to be on the other urls.py



]
