from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, reverse, redirect
from user_auth.decorators import auth_or_not
from .forms import ProfileUpdationForm
from .models import *
# Create your views here.

#Helper Functions
def deleteIncompleteDonations(user):
	"""
	Delete donations that are incomplete
	"""
	donation_requests = []
	incomplete_donations = Donation_made.objects.filter(status = 'Incomplete')
	for i in incomplete_donations:
		i.donation_request.amount_received -= i.amount
		i.donation_request.save()

	Donation_made.objects.filter(status = 'Incomplete').delete()

def retrieveWithDate(request):
	"""
	Return donations with proper date, since OR filter mixed the results
	"""
	all_donations = Donation_made.objects.all()
	current_user = request.user
	user_donations = []
	for donation in all_donations:
		if(donation.from_user == current_user or donation.to_user == current_user):
			user_donations.append(donation)
	return reversed(user_donations)

@login_required(login_url='user-auth:login')
@auth_or_not(1)
def userDashboard(request, pk):
	"""
	User Dashboard
	"""
	if(pk =='None'):
		return redirect('/')
	user = User.objects.get(id = pk)
	deleteIncompleteDonations(user)
	all_donations = retrieveWithDate(request)
	donations_made_count = Donation_made.objects.filter(from_user = user).count()
	donations_received_count = Donation_made.objects.filter(to_user = user).count()

	all_donations_count = donations_made_count + donations_received_count
	
	context = {'user':user, 'donations_made_count':donations_made_count, 'all_donations':all_donations, 
	'donations_received_count':donations_received_count}
	return render(request, 'accounts/user_dashboard.html', context)

@login_required(login_url='user_auth:login')
@auth_or_not(1)
def profileView(request):
	"""
	Profile View
	"""
	user = request.user
	form = ProfileUpdationForm()

	if request.method == "POST":
		form = ProfileUpdationForm(request.POST, request.FILES, instance=user)
		if form.is_valid():
			form.save()
		return redirect('/')
	
	context = {'user':user, 'form':form}
	return render(request, 'accounts/profile.html', context)