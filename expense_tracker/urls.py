from django.urls import path
from .views import TransactionListView, TransactionCreateView, TransactionUpdateView, TransactionDeleteView
from . import views

urlpatterns = [
    path('', views.home, name='tracker-home'),
    path('history/', TransactionListView.as_view(), name='transaction-history'),
    path('new/', TransactionCreateView.as_view(), name='transaction-create'),
    path('edit/<int:pk>/', TransactionUpdateView.as_view(), name='transaction-update'),
    path('delete/<int:pk>/', TransactionDeleteView.as_view(), name='transaction-delete'),
    path('about/', views.about, name='tracker-about'),
    path('contact/', views.contact, name='tracker-contact')
]