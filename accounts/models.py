from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import random

# Create your models here.

class User(AbstractUser):
	id =  					 		models.AutoField(primary_key=True)
	user_phone = 					models.CharField(max_length=200, unique=True, null=True, blank=True)
	user_other = 					models.CharField(max_length=200, null=True, blank=True)
	user_profile_image = 			models.ImageField(null=True, upload_to='profiles', blank=True, default='profiles/default-image.jpg')

	def __str__(self):
		return self.username

class Donation_Request(models.Model):
	payment_options = (
		('G-Pay', 'G-Pay'),
		('PayPal', 'PayPal'),
		('Paytm', 'Paytm'),
		)
	id =  					 	models.AutoField(primary_key=True)
	title = 					models.CharField(max_length=1000, null=True)
	user = 						models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name = 'user_donation_request')
	goal = 						models.PositiveIntegerField(null=True)
	amount_received = 			models.PositiveIntegerField(default=0, blank=True)
	description = 				models.TextField(null=True)
	updates = 					models.TextField(default="", blank=True)
	status = 					models.CharField(max_length=10, default='active')
	short_description = 		models.CharField(max_length=50, null=True, blank=True)
	request_image = 			models.ImageField(null=True, upload_to='donations', default='donations/default-image.jpg')

	def __str__(self):
		return self.title

class Donation_made(models.Model):
	id =  					 	models.AutoField(primary_key=True)
	from_user = 				models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='from_user_donations_made')
	to_user = 					models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='to_user_donations_made')
	donation_request = 			models.ForeignKey(Donation_Request, on_delete = models.SET_NULL, null = True, related_name = 'donation_request_donations_made')
	amount = 					models.PositiveIntegerField(null=True)
	note = 						models.CharField(max_length=200, null=True, blank=True)
	status = 					models.CharField(max_length = 10, default = 'Incomplete')
	donation_id = 				models.CharField(unique=True, max_length=100, null=True, blank=True, default=None) 
	datetime_of_payment = 		models.DateTimeField(default=timezone.now)
	razorpay_order_id = 		models.CharField(max_length=500, null=True, blank=True)
	razorpay_payment_id =	 	models.CharField(max_length=500, null=True, blank=True)
	razorpay_signature = 		models.CharField(max_length=500, null=True, blank=True)
 
	def __str__(self):
		return (self.from_user.username + ' to ' + self.to_user.username)

	def save(self, *args, **kwargs):
		if self.donation_id is None and self.id and self.datetime_of_payment:
			self.donation_id = self.datetime_of_payment.strftime('DONATION%Y%m%dODR') + str(self.id)
		return super().save(*args, **kwargs)