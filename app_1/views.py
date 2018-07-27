from django.shortcuts import render, redirect
from .models import User, Quote, Add
from django.contrib import messages

def index(request):
    return render(request, 'app_1/index.html')

def register(request):
    results = User.objects.register(request.POST)
    if results[0]:
        request.session["user_id"] = results[1].id
        request.session["first_name"] = results[1].first_name
        # request.session["last_name"] = results[1].id
        # return redirect("/dashbord")
        return redirect("/dashbord")
    else:
        for error in results[1]:
            messages.add_message(request, messages.ERROR, error)
    print (User)
    return redirect("/")


def login(request):
    results = User.objects.login(request.POST)
    if results[0]:
        request.session["user_id"] = results[1].id
        request.session["first_name"] = results[1].first_name
        # request.session["last_name"] = results[1].id
        # return redirect("/dashbord")
        return redirect("/dashbord")
    else:
        for error in results[1]:
            messages.add_message(request, messages.ERROR, error)
    return redirect("/")

def logout(request):
    request.session.clear()
    return redirect("/")

def dashbord(request):
    if "user_id" not in request.session:
        messages.add_message(request, messages.ERROR, "You need to login first")
        return redirect("/")
    all_quotes = Quote.objects.all()
    fav_quotes = Add.objects.filter(user=request.session["user_id"])
    
    for fav in fav_quotes:
        all_quotes = all_quotes.exclude(id=fav.quote.id)

    data = {
        "all_quotes": all_quotes,
        "fav_quotes": fav_quotes
    }
    return render(request, "app_1/dashbord.html", data)

def favorite(request, quote_id):
    # Trip.objects.join(trip_id, request.session["user_id"])
    Add.objects.add_quote(quote_id, request.session["user_id"])
    # return redirect("/travels/{}".format(request.session["user_id"]))
    return redirect('/dashbord')

def create(request):
    # print(request.session["user_id"])
    # print(request.POST['user_id'])
    results = Quote.objects.q(request.POST)
    if results[0]:
        return redirect("/dashbord")
    else:
        for error in results[1]:
            messages.add_message(request, messages.ERROR, error)
    return redirect ('/dashbord')
    # return render(request, 'app_1/add.html')

def view(request, addby_id):
    # user=User.objects.exclude(id=user_id)
    data={
        'quote': Quote.objects.filter(addby=addby_id),
        'count': Quote.objects.filter(addby=addby_id).count(),
        'name': User.objects.get(id=addby_id)
    }
    return render(request, 'app_1/view.html',data)

def remove(request, quote_id):
    x=Add.objects.filter(quote_id=quote_id).filter(user_id=request.session["user_id"])
    x.delete()
    # return redirect("/travels/{}".format(request.session["user_id"]))
    return redirect('/dashbord')
# 'quote':Quote.objects.get(id=quote_id),