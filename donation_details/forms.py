from django.forms import ModelForm
from accounts.models import Donation_Request

class DonationRequestForm(ModelForm):
	class Meta:
		model = Donation_Request
		fields = ['title', 'goal', 'description', 'request_image']