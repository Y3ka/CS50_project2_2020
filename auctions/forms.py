from django.forms import ModelForm
from django.forms import FloatField, Textarea
from auctions.models import Auction, Bid, Comment

class AuctionForm(ModelForm):
    class Meta:
        model = Auction
        fields = ['title', 'description', 'starting_price', 'picture', 'category']
    
class BidForm(ModelForm):
    bid = FloatField(label='')
    class Meta:
        model = Bid
        fields = ['bid']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['title', 'text']