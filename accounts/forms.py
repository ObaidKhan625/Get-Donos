from django.forms import ModelForm
from .models import Customer

class ProfileUpdationForm(ModelForm):
	class Meta:
		model = Customer
		fields = ['user_name', 'phone', 'email', 'other', 'profile_image']