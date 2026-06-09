from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create-order/', views.create_order, name='create_order'),
    path('verify-payment/', views.verify_payment, name='verify_payment'),
    path('<int:order_id>/success/', views.payment_success, name='payment_success'),
    path('<int:order_id>/failed/', views.payment_failed, name='payment_failed'),
]
