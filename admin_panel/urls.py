from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='admin_dashboard'),
    path('sellers/', views.seller_list_view, name='admin_sellers'),
    path('sellers/toggle/<int:seller_id>/', views.toggle_seller_status, name='toggle_seller_status'),
    path('sellers/pending/', views.pending_sellers_view, name='admin_pending_sellers'),
    path('seller-requests/', views.seller_requests_view, name='admin_seller_requests'),
    path('seller-requests/approve/<int:request_id>/', views.approve_seller_request, name='approve_seller_request'),
    path('suspended-sellers/', views.suspended_sellers_view, name='admin_suspended_sellers'),
    path('sellers/remove/<int:seller_id>/', views.remove_seller_status, name='remove_seller_status'),
    path('suspended-sellers/restore/<int:seller_id>/', views.restore_seller_status, name='restore_seller_status'),
    path('suspended-sellers/reactivate/<int:seller_id>/', views.reactivate_seller_status, name='reactivate_seller_status'),






    
]


# python3 manage.py makemigrations
# python3 manage.py migrate
# python3 manage.py runserver