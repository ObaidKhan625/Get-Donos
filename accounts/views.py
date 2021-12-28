from django.shortcuts import render, reverse, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from user_auth.decorators import auth_or_not
from .forms import ProfileUpdationForm
# Create your views here.

def deleteIncompleteDonations(user):
	donation_requests = []
	incomplete_donations = Donation_made.objects.filter(status = 'Incomplete')
	for i in incomplete_donations:
		i.donation_request.amount_received -= i.amount
		i.donation_request.save()

	Donation_made.objects.filter(status = 'Incomplete').delete()


@login_required(login_url='user-auth:login')
@auth_or_not(1)
def userDashboard(request, pk):
	user = User.objects.get(id = pk)
	deleteIncompleteDonations(user)
	all_donations = reversed(Donation_made.objects.all())
	donations_made_count = Donation_made.objects.filter(from_user = user).count()
	donations_received_count = Donation_made.objects.filter(to_user = user).count()
	all_donations_count = donations_made_count + donations_received_count
	donation_row_break = zip([i for i in range(1, all_donations_count+1)], all_donations)

	context = {'user':user, 'donations_made_count':donations_made_count, 'all_donations':all_donations, 
	'donations_received_count':donations_received_count, 'donation_row_break':donation_row_break}
	return render(request, 'accounts/user_dashboard.html', context)

@login_required(login_url='user_auth:login')
@auth_or_not(1)
def profileView(request):
	user = request.user
	form = ProfileUpdationForm()
	if request.method == "POST":
		form = ProfileUpdationForm(request.POST, request.FILES, instance=user)
		if form.is_valid():
			form.save()
		return redirect('/')
	context = {'user':user, 'form':form}
	return render(request, 'accounts/profile.html', context)