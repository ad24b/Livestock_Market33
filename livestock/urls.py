from django.urls import path
from . import views 
urlpatterns = [
    path('add/', views.add_livestock_view, name='add_livestock'),
    path('list/', views.list_livestock_view, name='list_livestock'),
    path('detail/<int:pk>/', views.livestock_detail, name='livestock_detail'), 

 # صفحة التفاصيل

]

#from .views import add_livestock_view, list_livestock_view , livestock_detail