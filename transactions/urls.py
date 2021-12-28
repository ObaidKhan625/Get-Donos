from django.urls import path
from . import views
app_name = 'transactions'

urlpatterns = [
      path('donation-page/<str:pk>/', views.donationPage, name='donation-page'),
      path('handlerequest/', views.handlerequest, name='handle-request'),
]