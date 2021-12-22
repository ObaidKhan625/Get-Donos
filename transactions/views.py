from django.shortcuts import render, redirect
from accounts.models import Donation_Request, Customer, Donation_made
from user_auth.decorators import auth_or_not
from django.http import JsonResponse, HttpResponse
import json

from django.contrib.sites.shortcuts import get_current_site
import razorpay

from GoFundMe import settings
razorpay_client = razorpay.Client(auth=(settings.razorpay_id, settings.razorpay_account_id))

# Create your views here.
@auth_or_not(1)
def donationPage(request, pk):
	donation_request = Donation_Request.objects.get(id = pk)
	updates = donation_request.updates
	donation_user = donation_request.user
	current_user = Customer.objects.get(user=request.user)
	progress_bar_widths = [((donation_request.amount_received/donation_request.goal)*100)]

	if request.method == "POST":
		if(current_user != donation_request.user):
			amount = int(request.POST.get('amount'))
			note = request.POST.get('note')
			donation = Donation_made.objects.create(from_user = current_user, to_user = donation_user, 
						amount = amount, note = note)
			donation_request.amount_received += amount
			donation_request.save()
			
			order_currency = 'INR'

			callback_url = 'http://'+ str(get_current_site(request))+"/login-passed/handlerequest/"
			print(callback_url)
			notes = {'order-type': "basic order from the website", 'key':'value'}
			razorpay_order = razorpay_client.order.create(dict(amount=amount*100, currency=order_currency, notes = notes, receipt=donation.donation_id, payment_capture='0'))
			print(razorpay_order['id'])
			donation.razorpay_order_id = razorpay_order['id']
			donation.save()
			
			return render(request, 'transactions/transaction_page.html', {'donation':donation, 
			'order_id': razorpay_order['id'], 'donationId':donation.donation_id, 
			'amount':amount, 'razorpay_merchant_id':settings.razorpay_id, 'callback_url':callback_url})
		else:
			update_added = request.POST.get('update-add')
			if(update_added == None):
				return redirect('/login-passed/donation-page/'+str(donation_request.id))
			updates = donation_request.updates+update_added+'\n'
			Donation_Request.objects.filter(id=pk).update(updates = updates)
			updates = updates.split('\n') if updates is not None else ""
			return redirect('/login-passed/donation-page/'+str(donation_request.id))
	updates = updates.split('\n') if updates is not None else ""
	updates.pop()
	context = {'donation_request':donation_request, 'donation_user':donation_user, 'updates':updates,
	'current_user':current_user, 'progress_bar_widths': progress_bar_widths}
	return render(request, 'transactions/donation_page.html', context)

@auth_or_not(1)
def transactionPage(request, pk):
	donation_request = Donation_Request.objects.get(id = pk)
	donation_user = donation_request.user
	amount = None
	note = None
	if request.method == "POST":
		body = json.loads(request.body.decode("utf-8"))
		amount = body.get('amount')
		note = body.get('note')
		from_user = Customer.objects.get(user=request.user)
		to_user = donation_request.user
		updated_amount = donation_request.amount_received+int(amount)
		Donation_Request.objects.filter(id=pk).update(amount_received = updated_amount)
		Donation_made.objects.create(from_user=from_user, to_user=to_user, amount=amount, note=note)
		return JsonResponse('Payment complete!', safe=False)
	context = {'amount':amount, 'note':note, 'donation_request':donation_request, 
	'donation_user':donation_user}
	return render(request, 'transactions/transaction_page.html', context)

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def handlerequest(request):
	if request.method == "POST":
		payment_id = request.POST.get('razorpay_payment_id', '')
		order_id = request.POST.get('razorpay_order_id','')
		signature = request.POST.get('razorpay_signature','')
		params_dict = { 
		'razorpay_order_id': order_id, 
		'razorpay_payment_id': payment_id,
		'razorpay_signature': signature
		}
		try:
			#print(order_id)
			order_db = Donation_made.objects.get(razorpay_order_id=order_id)
		except:
			return HttpResponse("505 Not Found")
		order_db.razorpay_payment_id = payment_id
		order_db.razorpay_signature = signature
		order_db.save()
		result = razorpay_client.utility.verify_payment_signature(params_dict)
		if result==None:
			amount = order_db.amount * 100   #we have to pass in paisa
			#try:
			print("Problem")
			print(payment_id, amount)
			razorpay_client.payment.capture(payment_id, amount)
			order_db.payment_status = 1
			order_db.save()
			data = {
				'order_id': order_db.donation_id,
				'transaction_id': order_db.razorpay_payment_id,
				'date': str(order_db.datetime_of_payment),
				'order': order_db,
				'amount': order_db.amount,
			}
			return render(request, 'transactions/paymentsuccess.html',{'id':order_db.id})
			"""
			except:
			order_db.payment_status = 2
			order_db.save()
			return render(request, 'transactions/paymentfailed.html')
			"""
		else:
			order_db.payment_status = 2
			order_db.save()
			return render(request, 'transactions/paymentfailed.html')
"""
except:
print("Fail 2")
return HttpResponse("505 not found")
"""