from django import forms
from decimal import Decimal
from auctions.models import Category

class ListingForm(forms.Form):
        title = forms.CharField(label="*Title", max_length=50)
        description = forms.CharField(
            label="*Description",
            max_length=200,
            widget=forms.Textarea)
        image = forms.URLField(
            label="Image URL",
            required=False
        )
        price = forms.DecimalField(label="*Starting Bid")
        category = forms.ModelChoiceField(
            queryset=Category.objects.all(),
            label="*Category"
        )

class BidForm(forms.Form):
    amount = forms.DecimalField(label="Bid")



class CommentForm(forms.Form):
    content = forms.CharField(label="Leave a Comment", max_length=50)


