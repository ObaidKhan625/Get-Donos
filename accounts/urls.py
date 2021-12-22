from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'accounts'

urlpatterns = [
	path('user-dashboard/<str:pk>/', views.userDashboard, name='user-dashboard'),
	path('profile-view/', views.profileView, name='profile-view'),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL,
	document_root=settings.MEDIA_ROOT)