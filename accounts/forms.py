from django.forms import ModelForm
from .models import User

class ProfileUpdationForm(ModelForm):
	class Meta:
		model = User
		fields = ['username', 'user_phone', 'email', 'user_other', 'user_profile_image']