from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *
from .forms import NewAuctionForm

def index(request):
    auctions_list = Auction.objects.all()
    category_list = Category.objects.all()
    # test = Auction.objects.get(id=4)
    # print(test)
    # print(request.user)
    # print(test.order_auction.filter(author=request.user))

    if request.user.is_authenticated:
        try:
            wish = WishList.objects.get(author=request.user).auction.all()
            orders = Orders.objects.filter(author=request.user).all()

            print(orders)
            print(auctions_list)
        except Exception as e:
            wish = None
            orders = None
    else:
        wish = None
        orders = None

    return render(request, "auctions/index.html",{
        "auctions": auctions_list,
        'category_list': category_list,
        'wish': wish,
        'orders': orders
    })

def categories(request, cat_id):
    category = Category.objects.get(pk=cat_id)
    auctions = Auction.objects.filter(category=category)
    category_list = Category.objects.all()
    return render(request, "auctions/categories.html",{
        'auctions': auctions,
        'category_list': category_list,
        'category': category
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

def auction(request, auc_id, messages=None):
    auction = Auction.objects.get(pk=auc_id)
    comments = Comment.objects.filter(auction=auction)
    bet = Bet.objects.filter(auction=auction).last()
    return render(request, 'auctions/auction.html',{
        'auction': auction,
        'comments': comments,
        'bet': bet,
        'message':messages
    })

def comment(request):
    if request.method == "POST":
        comment = request.POST["comment"]
        auc_id = int(request.POST["auction"])
        auction = Auction.objects.get(pk=auc_id)
        #author = User.objects.get(username=request.user.username)
        author = User.objects.get(username=request.user)
        #author = User.objects.get(pk=request.user.id)
        obj = Comment(auction=auction, author=author, content=comment)
        obj.save()
        return HttpResponseRedirect(reverse("auction", args=[auc_id]))

def bet(request):
    if request.method == 'POST':
        value = request.POST["bet"]
        author = User.objects.get(username=request.user)
        aauction = Auction.objects.get(pk=request.POST["auction_id"])
        auc_bet = Bet(auction=aauction, author=author, value=value)
        try:
            auc_bet.save()
            return HttpResponseRedirect(reverse('auction', args=[aauction.id]))
        except ValidationError as err:
            messages = err.messages[0].lstrip("['").rstrip("']")
            return auction(request,aauction.id,messages)


def wishlist(request):
    if request.method == 'POST':
        numb = int(request.POST["auc_id"])
        auction = Auction.objects.get(id=numb)
        author = User.objects.get(username=request.user)
        x = WishList.objects.filter(author=author).exists()
        if not x:
            wish = WishList(author=author)
            wish.save()
            wish.auction.add(auction)
            wish.save()
        else:
            wish = WishList.objects.get(author=request.user)
            wish.auction.add(auction)
            wish.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

    if request.method == 'GET':
        try:
            wish = WishList.objects.get(author=request.user)
        except: wish = None
        return render(request, "auctions/wishlist.html",{
            "auctions": wish.auction.all() if wish else None
        })

def wishlist_remove(request):
    if request.method == 'POST':
        numb = int(request.POST["auc_id"])
        auction = Auction.objects.get(id=numb)
        wish = WishList.objects.get(author=request.user)
        wish.auction.remove(auction)
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

def orders(request):
    if request.method == 'POST':
        numb = int(request.POST["auc_id"])
        auction = Auction.objects.get(id=numb)
        author = User.objects.get(username=request.user)
        x = Orders.objects.filter(author=author, auction=auction).exists()
        if not x:
            order = Orders(author=author, auction=auction)
            print(order)
            order.save()
        else:
            order = Orders.objects.get(author=author, auction=auction)
            order.quantity +=1
            order.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

    if request.method == 'GET':
        try:
            orders = Orders.objects.filter(author=request.user)
            print('*'*80)
            print(orders)
        except: orders = None
        return render(request, "auctions/orders.html", {
            "orders": orders
        })

def order_remove(request):
    if request.method == 'POST':
        numb = int(request.POST["auc_id"])
        order = Orders.objects.get(id=numb)
        order.quantity -= 1
        order.save()
        if order.quantity <= 0:
            order.delete()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

def add_auction(request):
    if request.method == 'GET':
        return render(request, 'auctions/add_auction.html', {
            'form': NewAuctionForm()
        })
    if request.method == 'POST':

        f = NewAuctionForm(request.POST, request.FILES)

        aauction = f.save(commit=False) # Create, but don't save the new auction instance.
        aauction.author = request.user # Modify the auction in some way.
        aauction.save() # Save the new instance.
        f.save_m2m() # Now, save the many-to-many data for the form.
        return HttpResponseRedirect(reverse("auction", args=[aauction.id]))

def edit(request):
    auc_id = int(request.POST['auc_id'])
    if request.method == 'POST':
        auction = Auction.objects.filter(author=request.user,id=auc_id).exists()
        if auction:
            auction_inst = Auction.objects.get(author=request.user,id=auc_id)
            return render(request, 'auctions/edit.html', {
                'form': NewAuctionForm(instance=auction_inst),
                'auc_id':auction_inst.id
            })

def update_auc(request):
    auc_id = int(request.POST['auc_id'])
    auction = Auction.objects.get(author=request.user, id=auc_id)
    f = NewAuctionForm(request.POST, instance=auction)
    f.save()
    return HttpResponseRedirect(reverse("auction", args=[auc_id]))

def cancel(request,auc_id):
    if request.method == 'POST':
        auction = Auction.objects.filter(author=request.user, id=auc_id).exists()
        if auction:
            auction_inst = Auction.objects.get(author=request.user, id=auc_id)
            auction_inst.state = 'c'
            auction_inst.winner = Bet.objects.filter(auction=auction_inst).last().author.username
            auction_inst.save()
            return HttpResponseRedirect(request.META['HTTP_REFERER'])

def resume(request, auc_id):
    if request.method == 'POST':
        auction = Auction.objects.filter(author=request.user, id=auc_id).exists()
        if auction:
            auction_inst = Auction.objects.get(author=request.user, id=auc_id)
            auction_inst.state = 'a'
            auction_inst.winner = ""
            auction_inst.save()
            return HttpResponseRedirect(request.META['HTTP_REFERER'])

def auction_remove(request):
    auc_id = int(request.POST['auc_id'])
    auction = Auction.objects.get(author=request.user, id=auc_id)
    auction.delete()
    return HttpResponseRedirect(reverse('wishlist'))


