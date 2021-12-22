from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from user_auth.decorators import auth_or_not
from accounts.models import *
from .forms import DonationRequestForm
from PIL import Image
import random

# Create your views here.

def exploreDonationRequests(request):
	class Row_counter:
		count = 0

		def increment(self):
			self.count += 1
			return ''

		def decrement(self):
			self.count -= 1
			return ''

		def double(self):
			self.count *= 2
			return ''
	donation_requests = Donation_Request.objects.filter(status='active')
	progress_bar_widths = []
	row_breaks = []

	for i in donation_requests:
		progress_bar_widths.append((i.amount_received/i.goal)*100)
	for i in range(3, len(donation_requests)+1, 3):
		row_breaks.append(i)
	
	donation_requests = zip(donation_requests, progress_bar_widths)
	context = {'donation_requests':donation_requests, 'row_counter': Row_counter(), 'row_breaks': row_breaks, 
	's': [1,2,3,4,5,6,7,8,9,10]}
	return render(request, 'donation_details/donation_requests.html', context)

@login_required(login_url='user-auth:login')
@auth_or_not(1)
def requestHistory(request, pk):
	user = User.objects.get(id = pk)
	profile = Customer.objects.get(user = user)
	donation_requests = Donation_Request.objects.filter(user = profile)
	total_donation_requests = donation_requests.count()
	donation_requests = reversed(donation_requests)
	context = {'user':user, 'profile':profile, 'donation_requests':donation_requests, 
	'total_donation_requests':total_donation_requests}
	return render(request, 'donation_details/request_history.html', context)

@login_required(login_url='user-auth:login')
@auth_or_not(1)
def createDonationRequest(request, pk):
	customer = Customer.objects.get(user=request.user)
	if request.method == "POST":
		form = DonationRequestForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			Donation_Request.objects.filter(user=None, status='active').update(user=customer)
			donation = Donation_Request.objects.filter(user=customer, status='active')
			description = donation.values_list('description', flat=True)[0]
			short_description = description[:400] + '....'
			Donation_Request.objects.filter(user=customer).update(short_description=short_description)
		return redirect('/login-passed/user-dashboard/'+str(request.user.id))
	else:
		Donation_Request.objects.filter(user = customer, status='active').update(status = 'closed')
		form = DonationRequestForm()
		context = {'form':form}
		return render(request, 'donation_details/create_donation_request_page.html', context)