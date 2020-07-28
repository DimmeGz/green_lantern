"""car_dealer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic import TemplateView

from apps.newsletters.views import NewsLetterView
from common.views import LoginView, logout_view
from apps.cars.views import CarListView, CarView
from apps.photos.views import UpdateImageView
from apps.orders.views import OrderView, OrderListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('success/', TemplateView.as_view(template_name='success.html'), name='success'),
    path('newsletter/', NewsLetterView.as_view(), name='newsletter'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('car_list/', CarListView.as_view(), name='car_list'),
    path('update_photo/', login_required(UpdateImageView.as_view()), name='update_photo'),
    path('car/<int:id>', CarView.as_view(), name='car_list'),
    path('order/', login_required(OrderView.as_view()), name='order'),
    path('order_list/', OrderListView.as_view(), name='order_list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
