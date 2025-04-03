from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from decimal import Decimal
from .models import *
from .forms import *

# PAGES PATH
PAGES = {
    "INDEX" :"auctions/index.html",
    "LOGIN" : "auctions/login.html",
    "REGISTER" : "auctions/register.html",
    "CATEGORIES": "auctions/categories.html",
    "LISTING" : "auctions/listing.html",
    "NEW" : "auctions/new.html",
    "WATCHLIST": "auctions/watchlist.html"
}


def index(request):
    PARAMETERS = {
        "active":True
    }

    CONTEXT = {
         "listings" : Listings.objects.filter(**PARAMETERS),
         "title": "Trending"
    }

    if category := request.GET.get('category'):
        PARAMETERS.update({
            "category": Category.objects.filter(name=category).first()
        })

        CONTEXT.update({
            "listings" : Listings.objects.filter(**PARAMETERS),
            "title": PARAMETERS['category'].name
        })


    return render(request, PAGES['INDEX'], CONTEXT)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # just_check_existence if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, PAGES['LOGIN'], {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, PAGES['LOGIN'])


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, PAGES['REGISTER'], {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, PAGES['REGISTER'], {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, PAGES['REGISTER'])


def listing_categories_view(request):
    CONTEXT = {
        "categories": Category.objects.all()
    }

    return render(request, PAGES['CATEGORIES'], CONTEXT)

def bid_view(request, listing_id):
    listing = Listings.objects.filter(pk=listing_id).first()

    CONTEXT = {
        "entries" : Bids.objects.filter(listing=listing),
        "form": BidForm(),
        "minimum_bid_amount" : listing.price + Decimal(0.5)
    }

    CONTEXT.update({
        "count": CONTEXT['entries'].count(),
        "leading": CONTEXT['entries'].order_by("-amount").first()
    })

    if CONTEXT['leading']:
        profit = (((CONTEXT['leading'].amount / listing.price) - 1) * 100)
        profit = round(profit, 2)
        CONTEXT.update({
            "premium": profit,
            "minimum_bid_amount": CONTEXT['leading'].amount + Decimal(0.5)
        })


    match request.method:
        case "POST":
            if request.user.is_anonymous:
                return HttpResponseRedirect(reverse("login"))

            CONTEXT.update({
                "form": BidForm(request.POST)
            })

            if listing.active == False:
                 messages.error(request, "Error: Unable to Bid - The Auction Has Already Ended!")

            elif not CONTEXT['form'].is_valid():
                messages.error(request, "Error: Missing Fields.")

            elif CONTEXT['form'].cleaned_data['amount'] < CONTEXT['minimum_bid_amount']:
                messages.error(request, "Error: Low Bid")

            elif request.user is listing.seller:
                messages.error(request, "Error: Unable to Bid in Own Auction!")

            else:
                Bids.objects.create(
                    bidder=request.user,
                    listing=listing,
                    amount=CONTEXT['form'].cleaned_data['amount']
                )
                messages.success(request, "Bid placed successfully!")

            return HttpResponseRedirect(reverse("auctions:listing", kwargs={"id": listing_id}))

        case "GET":
            return CONTEXT

def comment_view(request, listing_id):
    listing = Listings.objects.filter(pk=listing_id).first()

    CONTEXT = {
        "entries":  Comments.objects.filter(listing=listing),
        "form": CommentForm()
    }

    match request.method:

        case "POST":
            if request.user.is_anonymous:
                return HttpResponseRedirect(reverse("login"))

            CONTEXT.update({
                "form" : CommentForm(request.POST)
            })

            if not CONTEXT['form'].is_valid():
                messages.error(request, "Failed to place comment")

            else:
                Comments.objects.create(commenter=request.user, listing=listing, content=CONTEXT['form'].cleaned_data['content'])
                messages.success(request, "Sucess! Your Comment Was Sent!")


            return HttpResponseRedirect(reverse("auctions:listing", kwargs={"id": listing_id}))

        case "GET":
            return CONTEXT


def listing_view(request, id):
    CONTEXT = {
        "listing": Listings.objects.filter(pk=id).first(),
        "bids": bid_view(request, listing_id=id),
        "comments" : comment_view(request, listing_id=id)
    }


    match request.method:
        case "POST":
            return bid_view(request, listing_id=id) if "bid_form" in request.POST else comment_view(request, listing_id=id) if "comment_form" in request.POST else None

        case "GET":
            if CONTEXT['listing'].active is False:
                messages.info(request, "This Auction Has Ended!")

            if request.user.is_authenticated:
                CONTEXT.update({
                    "watchlisted": watchlist_view(request, listing_id=id, just_check_existence=True),
                })

            return render(request, PAGES['LISTING'], CONTEXT)

@login_required
def watchlist_view(request, listing_id=None, just_check_existence=False):
    CONTEXT = {
        "watchlist": Watchlist.objects.filter(user=request.user)
    }

    listing = Listings.objects.filter(pk=listing_id).first()

    match just_check_existence:
        case True:
            return entry if (entry := CONTEXT["watchlist"].filter(listing=listing).first()) else None
        case False:
            match request.method:
                case "POST":
                    if entry := watchlist_view(request, listing_id, just_check_existence=True):
                        entry.delete()
                    else:
                        Watchlist.objects.create(user=request.user, listing=listing)

                    return HttpResponseRedirect(reverse("auctions:listing", kwargs={"id":listing_id}))

                case "GET":
                    return render(request, PAGES['WATCHLIST'], CONTEXT)






@login_required
def new_listing(request):
    CONTEXT = {
        "form": ListingForm()
    }

    match request.method:
        case "POST":
            CONTEXT.update({
                "form" : ListingForm(request.POST)
            })

            if CONTEXT['form'].is_valid():
                Listings.objects.create(seller=request.user, **CONTEXT['form'].cleaned_data)

            return HttpResponseRedirect(reverse("auctions:index"))

        case "GET":
            return render(request, PAGES['NEW'], CONTEXT)

@login_required
def close_listing(request, id):
    match request.method:
        case "POST":
            listing = Listings.objects.filter(pk=id).first()
            if request.user is listing.seller:
                 listing.active = False
                 listing.save()
            else:
                messages.error(request, "Only the listing owner can end the auction.")

            return HttpResponseRedirect(reverse("auctions:index"))



