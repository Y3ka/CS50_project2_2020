from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Auction(models.Model):

    categories = [
        ('Vehicules', 'Vehicules'),
        ('Weapons', 'Weapons'),
        ('Books', 'Books'),
        ('Multimedia', 'Multimedia'),
        ('Others', 'Others')
    ]
    user = models.CharField(max_length=30, null=True)
    title = models.CharField(max_length=50)
    description = models.TextField()
    starting_price = models.FloatField(default=0)
    last_bid = models.ForeignKey('Bid', on_delete=models.CASCADE, null=True)
    picture = models.URLField()
    category = models.CharField(max_length=30, default="", choices=categories)
    closed = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.title} | Starting price: {self.starting_price} | Last bid: {self.last_bid}"

class Bid(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    bid = models.FloatField()
    date = models.DateTimeField(blank=False, auto_now_add=True)
    
    def __str__(self):
        return f"{self.user} at {self.date} | {self.bid}"

class Comment(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    text = models.TextField()
    date = models.DateField(auto_now_add=True)
    auction = models.ForeignKey("Auction", on_delete= models.CASCADE, null=True)

    def __str__(self):
        return f"{self.title} by {self.user} at {self.date}"

class Watchlist(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    auctions = models.ManyToManyField('Auction')

    def __str__(self):
        return f"{self.auctions}"