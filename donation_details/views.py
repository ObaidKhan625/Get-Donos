from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from user_auth.decorators import auth_or_not
from accounts.models import *
from .forms import DonationRequestForm
from PIL import Image
import random

# Create your views here.

def deleteIncompleteDonations(user):
	donation_requests = []
	incomplete_donations = Donation_made.objects.filter(status = 'Incomplete')
	for i in incomplete_donations:
		i.donation_request.amount_received -= i.amount
		i.donation_request.save()

	Donation_made.objects.filter(status = 'Incomplete').delete()

def exploreDonationRequests(request):
	deleteIncompleteDonations(request.user)
	donation_requests = Donation_Request.objects.filter(status='active')
	progress_bar_widths = []

	for i in donation_requests:
		progress_bar_widths.append((i.amount_received/i.goal)*100)
	
	donation_requests = zip(donation_requests, progress_bar_widths)
	context = {'donation_requests':donation_requests}
	return render(request, 'donation_details/donation_requests.html', context)

@login_required(login_url='user-auth:login')
@auth_or_not(1)
def requestHistory(request, pk):
	user = User.objects.get(id = pk)
	deleteIncompleteDonations(user)
	donation_requests = Donation_Request.objects.filter(user = user)
	total_donation_requests = donation_requests.count()
	donation_requests = reversed(donation_requests)
	context = {'user':user, 'donation_requests':donation_requests, 
	'total_donation_requests':total_donation_requests}
	return render(request, 'donation_details/request_history.html', context)

@login_required(login_url='user-auth:login')
@auth_or_not(1)
def createDonationRequest(request, pk):
	if request.method == "POST":
		form = DonationRequestForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			Donation_Request.objects.filter(user=None, status='active').update(user=request.user)
			donation = Donation_Request.objects.filter(user=request.user, status='active')
			description = donation.values_list('description', flat=True)[0]
			short_description = description[:400] + '....'
			Donation_Request.objects.filter(user=request.user).update(short_description=short_description)
		return redirect('/login-passed/user-dashboard/'+str(request.user.id))
	else:
		Donation_Request.objects.filter(user = request.user, status='active').update(status = 'closed')
		form = DonationRequestForm()
		context = {'form':form}
		return render(request, 'donation_details/create_donation_request_page.html', context)