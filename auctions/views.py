from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Auction, Comment, Bid, Watchlist
from .forms import AuctionForm, BidForm, CommentForm


def index(request):
    return render(request, "auctions/index.html", {
        "auctions": Auction.objects.filter(closed=False),
        "closed": False
    })

def closed_index(request):
    return render(request, "auctions/index.html", {
        "auctions": Auction.objects.filter(closed=True),
        "closed": True
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
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def listing(request, listing):
    """
    Print the listing
    """
    auction = Auction.objects.get(title=listing)
    try:
        in_watchlist = auction in Watchlist.objects.get(user=request.user).auctions.all()
        watchlist_empty = False
    except:
        in_watchlist = False
        watchlist_empty = True
    comments = Comment.objects.filter(auction=auction)
    print(comments)
    #the user either post a bid, or a comment, or add to watchlist
    if request.method == "POST":
        bid = BidForm(request.POST)
        comment = CommentForm(request.POST)
        if bid.is_valid():
            new_bid = bid.save(commit=False)
            try:
                if new_bid.bid < auction.last_bid.bid:
                    comment_form = CommentForm()
                    return render(request, "auctions/listing.html", {
                        "auction": auction,
                        "bid_form": bid,
                        "comment_form": comment_form,
                        "comments": comments,
                        "errorBid": True,
                        "in_watchlist": in_watchlist
                    })
            except AttributeError:
                if new_bid.bid <= auction.starting_price:
                    comment_form = CommentForm()
                    return render(request, "auctions/listing.html", {
                        "auction": auction,
                        "bid_form": bid,
                        "comment_form": comment_form,
                        "comments": comments,
                        "errorBid": True,
                        "in_watchlist": in_watchlist
                    })
            try:
                new_bid.user = request.user
                new_bid.save()
                #update the last bid of auction
                auction.last_bid = new_bid
                auction.save()
            except ValueError:
                bid_form = BidForm()
                comment_form = CommentForm()
                return render(request, "auctions/listing.html", {
                    "auction": auction,
                    "bid_form": bid_form,
                    "comment_form": comment_form,
                    "comments": comments,
                    "errorBid2": True,
                    "in_watchlist": in_watchlist
                })
        elif comment.is_valid():
            new_comment = comment.save(commit=False)
            try:
                new_comment.user = request.user
                new_comment.auction = auction
                new_comment.save()
            except ValueError:
                bid_form = BidForm()
                comment_form = CommentForm()
                return render(request, "auctions/listing.html", {
                    "auction": auction,
                    "bid_form": bid_form,
                    "comment_form": comment_form,
                    "comments": comments,
                    "errorComment": True,
                    "in_watchlist": in_watchlist
                })
            
        elif "close" in request.POST:
            auction.closed = True
            auction.save()
        else:
            #add the item to watchlist or remove if it is already in it
            if in_watchlist:
                watchlist = Watchlist.objects.get(user=request.user)
                watchlist.auctions.remove(auction)
            elif watchlist_empty:
                watchlist = Watchlist.objects.create(user=request.user)
                watchlist.auctions.add(auction)
            else:
                watchlist = Watchlist.objects.get(user=request.user)
                watchlist.auctions.add(auction)
            watchlist.save()
            bid_form = BidForm()
            comment_form = CommentForm()
            return render(request, "auctions/listing.html", {
                "auction": auction,
                "bid_form": bid_form,
                "comment_form": comment_form,
                "comments": comments,
                "in_watchlist": not in_watchlist
            })
    bid_form = BidForm()
    comment_form = CommentForm()
    return render(request, "auctions/listing.html", {
        "auction": auction,
        "bid_form": bid_form,
        "comment_form": comment_form,
        "comments": comments,
        "in_watchlist": in_watchlist
    })

def create(request):
    if request.method == "POST":
        auction = AuctionForm(request.POST)
        if auction.is_valid():
            new_auction = auction.save(commit=False)
            new_auction.user = request.user.username
            new_auction.save()
        else:
            return render(request, "auctions/create.html", {
                "form": auction
            })
    form = AuctionForm()
    return render(request, "auctions/create.html", {
        "form": form
    })

def watchlist(request):
    """
    Print the user's watchlist
    """
    try: 
        auction = Watchlist.objects.get(user=request.user).auctions.all()
        return render(request, "auctions/watchlist.html", {
            "auctions": auction
        })
    except:
        print("test")
        return render(request, "auctions/watchlist.html", {
            "auctions": []
        })

def categories(request):
    """
    Print all the categories
    """
    categories = ["Vehicules","Books","Weapons","Multimedia", "Others"]
    return render(request, "auctions/categories.html", {
        "categories": categories,
    })

def category(request, category):
    """
    Print the listing in the corresponding category
    """
    auctions_list = Auction.objects.filter(category=category)
    return render(request, "auctions/category.html", {
        "auctions": auctions_list,
        "category": category,
    }) 