from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    first_name = models.CharField(max_length=64, default ="")
    last_name = models.CharField(max_length=64, default = "")
    email = models.EmailField(max_length=254)
    #username = models.CharField(max_length=30, default = "")
    password = models.CharField(max_length = 1000, default = "")
    def __str__(self):
        return self.username + ": " + self.first_name + " " + self.last_name 

class Listing(models.Model):
    current_bid = models.DecimalField(default = 0.00, max_digits = 64, decimal_places=2)
    name = models.CharField(max_length =64, default = "")
    description = models.CharField(max_length=400, default = "")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "seller")
    category = models.CharField(max_length = 64, default = "No Category Listed")
    picture = models.ImageField(upload_to = 'static/auctions/listingimgs/',  default = 'default-image.jpg')
    def __str__(self):
        return self.seller.first_name + "'s " + self.name
class Bid(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name = "item")
    amount = models.DecimalField(default = 0.00, max_digits = 64, decimal_places = 2)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "buyer", null = True)
    def __str__(self):
        return "Bid on " + self.item.name + "by " + self.buyer.first_name + ": " + str(self.amount)
class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name = "listing")
    time = models.DateTimeField(auto_now=True)
    commenter = models.ForeignKey(User, on_delete= models.CASCADE, related_name = "commenter")
    content = models.CharField(max_length=255, default = "")
    def __str__(self):
        return self.commenter.first_name + "'s comment on " + self.listing.name + " (" + str(self.time) + ")"
class Watchlist(models.Model): 
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "watcher", null = True)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name = "watchitem", null = True)
    def __str__(self):
        return self.user.first_name + ": " + self.item.name
