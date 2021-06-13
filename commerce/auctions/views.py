from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Listing, Bid, Comment, Watchlist
from django.templatetags.static import static
from datetime import datetime

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            request.session["user_email"] = user.email
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            request.session["user_email"] = user.email
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
@login_required(login_url = 'login')
def create_listing(request):
    return render(request, "auctions/createlisting.html", {
        
    })
@login_required(login_url = 'login')
def post_listing(request):
    try: 
        item = Listing(current_bid = request.POST['starting_bid'], name = request.POST['listing_name'], description = request.POST['description'], seller = User.objects.get(email = request.session["user_email"]), category = request.POST['category'], picture = request.FILES['picture'])
    except: 
        item = Listing(current_bid = request.POST['starting_bid'], name = request.POST['listing_name'], description = request.POST['description'], seller = User.objects.get(email = request.session["user_email"]), category = request.POST['category'])

    item.save()
    return HttpResponseRedirect(reverse("index"))
@login_required(login_url = 'login')
def product_page(request): 
    highest_bidder = False
    try: 
        if Bid.objects.latest('amount').buyer.id == User.objects.get(email = request.session["user_email"]).id:
            highest_bidder = True
    except:
        pass

    listing = Listing.objects.get(id =request.POST['listing'])
    return render(request, "auctions/product_page.html", {
        "listing": Listing.objects.get(id =request.POST['listing']),
        "message": "",
        "highest_bidder": highest_bidder,
        "comments": Comment.objects.filter(listing = listing)
    })
@login_required(login_url = 'login')
def bid(request):
    listing = Listing.objects.get(id = request.POST['listing'])
    message = ""
    highest_bidder = False
    try: 
        if Bid.objects.latest('amount').buyer.id == User.objects.get(email = request.session["user_email"]).id:
            highest_bidder = True
    except: 
        pass
    try:
        bid = float(request.POST['bid'])
    except: 
        message = "Please enter a numerical bid"
        return render(request, "auctions/product_page.html", {
        "listing": listing,
        "message": message,
        "highest_bidder": highest_bidder
        })
    if bid > listing.current_bid:
        listing.current_bid = format(bid, '.2f')
        message = "Bid submitted successfully"
        listing.save()
        new_bid = Bid(item = listing, amount = bid, buyer = User.objects.get(email = request.session["user_email"]))
        new_bid.save()
        highest_bidder = True
    else:
        message = "Please enter a bid higher than the current amount"
    return render(request, "auctions/product_page.html", {
        "listing": listing,
        "message": message,
        "highest_bidder": highest_bidder
    })
@login_required(login_url = 'login')
def add_watchlist(request):

    listing = Listing.objects.get(id = request.POST['listing'])
    message = ""

    if request.POST['index'] == "True":
        if Watchlist.objects.filter(user = User.objects.get(email = request.session["user_email"]), item = listing).exists():
            message = "Already added to watchlist"
            return render(request, "auctions/index.html", {
            "listings": Listing.objects.all(),
            "message": message,
            })

        message = "Added to watchlist"
   
        watch_me = Watchlist(item = listing, user = User.objects.get(email = request.session["user_email"]))
        watch_me.save()
        return render(request, "auctions/index.html", {
            "listings": Listing.objects.all(),
            "message": message,
        })
    
    highest_bidder = False
    try: 
        if Bid.objects.latest('amount').buyer.id == User.objects.get(email = request.session["user_email"]).id:
            highest_bidder = True
    except: 
        pass

    if Watchlist.objects.filter(user = User.objects.get(email = request.session["user_email"]), item = listing).exists():
        message = "Already added to watchlist"
        return render(request, "auctions/product_page.html", {
        "listing": listing,
        "message": message,
        "highest_bidder": highest_bidder
        })

    message = "Added to watchlist"
   
    watch_me = Watchlist(item = listing, user = User.objects.get(email = request.session["user_email"]))
    watch_me.save()
    return render(request, "auctions/product_page.html", {
        "listing": listing,
        "message": message,
        "highest_bidder": highest_bidder
    })
def watchlist(request):
    buyer = User.objects.get(email = request.session["user_email"])
    listings = []
    message = ""
    watchlist = Watchlist.objects.filter(user=buyer)
    for item in watchlist: 
        listings.append(item.item)
    return render(request, "auctions/watchlist.html", {
        "listings": listings,
        "message": message
    })

def remove_watchlist(request):
    Watchlist.objects.filter(item  = Listing.objects.get(id = request.POST['listing']), user = User.objects.get(email = request.session["user_email"])).delete()
    listings = []
    message = "Item removed from Watchlist"
    watchlist = Watchlist.objects.filter(user=User.objects.get(email = request.session["user_email"]))
    for item in watchlist: 
        listings.append(item.item)
    return render(request, "auctions/watchlist.html", {
        "listings": listings,
        "message": message
    })
def categories(request):
    listings = Listing.objects.all().iterator()
    cats = []
    while True:
        try:
            listing = next(listings)
            if listing.category not in cats:
                cats.append(listing.category)
        except StopIteration:
            break
    return render(request, "auctions/categories.html", {
        "categories": cats
    })
def category(request, items):
    return render(request, "auctions/category.html", {
        "listings": Listing.objects.filter(category = items),
        "item": items
    })
def search(request):
    item = request.POST['query'] 
    listings = Listing.objects.all()
    filtered_listings = []
    for listing in listings: 
        if item.lower() in listing.name.lower():
            filtered_listings.append(listing)
            
    return render(request, "auctions/index.html", {
        "listings": filtered_listings
    })

def comment(request):
    new_comment = Comment(listing = Listing.objects.get(id = request.POST['listing']), content = request.POST['content'], time = datetime.now(), commenter =User.objects.get(email = request.session["user_email"]) )    
    new_comment.save()
    highest_bidder = False
    try: 
        if Bid.objects.latest('amount').buyer.id == User.objects.get(email = request.session["user_email"]).id:
            highest_bidder = True
    except:
        pass
    listing = Listing.objects.get(id =request.POST['listing'])
    return render(request, "auctions/product_page.html", {
        "listing": Listing.objects.get(id =request.POST['listing']),
        "message": "",
        "highest_bidder": highest_bidder,
        "comments": Comment.objects.filter(listing = listing)
    })