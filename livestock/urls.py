from django.urls import path
from .views import add_livestock_view, list_livestock_view , livestock_detail

urlpatterns = [
    path('add/', add_livestock_view, name='add_livestock'),
    path('list/', list_livestock_view, name='list_livestock'),
    path('detail/<int:pk>/',livestock_detail, name='livestock_detail'),  # صفحة التفاصيل
]
