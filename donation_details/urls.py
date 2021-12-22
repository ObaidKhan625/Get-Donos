from django.urls import path
from . import views
app_name = 'donation_details'

urlpatterns = [
	path('explore-donations/', views.exploreDonationRequests, name='explore-donations'),
	path('request-history/<str:pk>/', views.requestHistory, name='request-history'),
	path('create-donation-request/<str:pk>/', views.createDonationRequest, name='create-donation-request'),
]