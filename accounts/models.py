from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import random

# Create your models here.

class Customer(models.Model):
	user = models.OneToOneField(User, null=True, unique=True, on_delete= models.CASCADE)
	user_name = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=200, unique=True, null=True, blank=True)
	email = models.CharField(max_length=200, unique=True, null=True, blank=True)
	other = models.CharField(max_length=200, null=True, blank=True)
	profile_image = models.ImageField(null=True, upload_to='profiles', blank=True, default='profiles/default-image.jpg')
	

	def __str__(self):
		return self.user_name

class Donation_made(models.Model):
	from_user = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, related_name='donation_from_user')
	to_user = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, related_name='donation_to_user')
	amount = models.PositiveIntegerField(null=True)
	note = models.CharField(max_length=200, null=True, blank=True)
	donation_id = models.CharField(unique=True, max_length=100, null=True, blank=True, default=None) 
	datetime_of_payment = models.DateTimeField(default=timezone.now)
	razorpay_order_id = models.CharField(max_length=500, null=True, blank=True)
	razorpay_payment_id = models.CharField(max_length=500, null=True, blank=True)
	razorpay_signature = models.CharField(max_length=500, null=True, blank=True)
 
	def __str__(self):
		return (self.from_user.user_name + ' to ' + self.to_user.user_name)

	def save(self, *args, **kwargs):
		if self.donation_id is None and self.id and self.datetime_of_payment:
			self.donation_id = self.datetime_of_payment.strftime('DONATION%Y%m%dODR') + str(self.id)
		return super().save(*args, **kwargs)

class Donation_Request(models.Model):
	payment_options = (
		('G-Pay', 'G-Pay'),
		('PayPal', 'PayPal'),
		('Paytm', 'Paytm'),
		)
	title = models.CharField(max_length=1000, null=True)
	user = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE)
	goal = models.PositiveIntegerField(null=True)
	amount_received = models.PositiveIntegerField(default=0, blank=True)
	description = models.TextField(null=True)
	updates = models.TextField(default="", blank=True)
	status = models.CharField(max_length=10, default='active')
	short_description = models.CharField(max_length=50, null=True, blank=True)
	request_image = models.ImageField(null=True, upload_to='donations', default='donations/default-image.jpg')

	def __str__(self):
		return self.title