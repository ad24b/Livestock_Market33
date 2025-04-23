from django.urls import path
from . import views 


urlpatterns = [
    path('buy-now/<int:pk>/', views.livestock_buy_now, name='livestock_buy_now'),
]
# from .views import buy_livestock,livestock_buy_now