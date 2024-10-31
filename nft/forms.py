from django.forms import ModelForm
from nft.models import Collection
from django import forms


class ImageForm(ModelForm):
    name = forms.CharField(
        label='Name',
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'InputName'})
    )
    quantity = forms.IntegerField(
        label='Quantity',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'InputQuantity', 'max': '10'})
    )

    class Meta:
        model = Collection
        fields = ["name"]
