from django.forms import ModelForm
from .models import *

class NewAuctionForm(ModelForm):
    class Meta:
        model = Auction
        fields = ['title','category','image','content', 'value']