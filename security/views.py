from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Stock, Stock_History_log
from .forms import *
from django.http import HttpResponse
import csv




def issue_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = IssueForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.receive_quantity = 0
        issue_quantity = instance.issue_quantity
        if instance.quantity < issue_quantity:
            messages.warning(request, "Issue quantity cannot be greater than current quantity.")
        else:
            while issue_quantity > instance.quantity:
                messages.warning(request, "Not enough stock available. Current quantity is " + str(instance.quantity))
                return redirect('/issue_items/'+str(instance.id))
            instance.quantity -= issue_quantity
            instance.issue_by = str(request.user)
            messages.success(request, "Issued SUCCESSFULLY. " + str(instance.quantity) + " " + str(instance.item_name) + "s now left in Store")
            instance.save()
            return redirect('/stock_detail/'+str(instance.id))

    context = {
        "title": 'Issue ' + str(queryset.item_name),
        "queryset": queryset,
        "form": form,
        "username": 'Issue By: ' + str(request.user),
    }
    return render(request, "add_items.html", context)


def receive_items(request, pk):
	queryset = Stock.objects.get(id=pk)
	form = ReceiveForm(request.POST or None, instance=queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.issue_quantity = 0
		instance.quantity += instance.receive_quantity
		instance.save()
		messages.success(request, "Received SUCCESSFULLY. " + str(instance.quantity) + " " + str(instance.item_name)+"s now in Store")

		return redirect('/stock_detail/'+str(instance.id))
		# return HttpResponseRedirect(instance.get_absolute_url())
	context = {
			"title": 'Reaceive ' + str(queryset.item_name),
			"instance": queryset,
			"form": form,
			"username": 'Receive By: ' + str(request.user),
		}
	return render(request, "add_items.html", context)


def delete_items(request, pk):
	queryset = Stock.objects.get(id=pk)
	if request.method == 'POST':
		queryset.delete()
		return redirect('/list_item')
	return render(request, 'delete_items.html')

def update_items(request, pk):
	queryset = Stock.objects.get(id=pk)
	form = StockUpdateForm(instance=queryset)
	if request.method == 'POST':
		form = StockUpdateForm(request.POST, instance=queryset)
		if form.is_valid():
			form.save()
			return redirect('/list_item')

	context = {
		'form':form
	}
	return render(request, 'add_items.html', context)

def add_items(request):
	form = StockCreateForm(request.POST or None)
	if form.is_valid():
		form.save()
		return redirect('/list_item')
	context = {
		"form": form,
		"title": "Add Item",
	}
	return render(request, "add_items.html", context)


def stock_detail(request, pk):
	queryset = Stock.objects.get(id=pk)
	context = {
		"title": queryset.item_name,
		"queryset": queryset,
	}
	return render(request, "stock_detail.html", context)



def list_item(request):
	title = 'List of Items'
	form = StockSearchForm(request.POST or None)
	queryset = Stock.objects.all()
	context = {
		"title": title,
		"queryset": queryset,
		"form":form
	}
	if request.method == 'POST':
		category = form['category'].value()
		queryset = Stock.objects.filter(
										item_name__icontains=form['item_name'].value()
										)
		if (category != ''):
			queryset = queryset.filter(category_id=category)

		context = {
		"form": form,
		"title": title,
		"queryset": queryset,
	}
	if form['export_to_CSV'].value() == True:
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="List of stock.csv"'
		writer = csv.writer(response)
		writer.writerow(['CATEGORY', 'ITEM NAME', 'QUANTITY'])
		instance = queryset
		for stock in instance:
			writer.writerow([stock.category, stock.item_name, stock.quantity])
		return response

	return render(request, "list_item.html", context)

def home(request):
	# check if logging in
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		# authenticate
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, 'Login Successfully!')
			return redirect('list_item')
		else:
			messages.success(request, 'Authentication Error!! Try Again!!')
			return redirect('home')
	else:		
		return render(request, 'home.html', {})

def logout_user(request):
	logout(request)
	messages.success(request, 'You have been logged out!!')
	return redirect('home')



def reorder_level(request, pk):
	queryset = Stock.objects.get(id=pk)
	form = ReorderLevelForm(request.POST or None, instance=queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "Reorder level for " + str(instance.item_name) + " is updated to " + str(instance.reorder_level))

		return redirect("/list_item")
	context = {
			"instance": queryset,
			"form": form,
		}
	return render(request, "add_items.html", context)


@login_required
def list_history(request):
	header = 'LIST OF ITEMS'
	queryset = StockHistory.objects.all()
	context = {
		"header": header,
		"queryset": queryset,
	}
	return render(request, "list_history.html",context)
