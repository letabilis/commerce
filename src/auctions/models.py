from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name

class Listings(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=False)
    description = models.TextField(blank=False)
    image = models.URLField(blank=True, max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    datetime = models.DateTimeField(auto_now_add=True, db_default=datetime.now())
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Listing: {self.title}\nCategory: {self.category} Seller: {self.seller}\nPrice: {self.price}\nDateTime: {self.datetime}"

class Bids(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listings, on_delete=models.RESTRICT)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=False)

class Comments(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE)
    content = models.TextField(blank=False)
    datetime = models.DateTimeField(auto_now_add=True, db_default=datetime.now())


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE)
