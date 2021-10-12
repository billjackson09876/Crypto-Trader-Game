from django import forms

from .models import Bank, Coins, Asset
from django.forms.widgets import NumberInput, SelectDateWidget

class TradeForm(forms.ModelForm):
	class Meta:
		model = Asset
		fields = ['quantity']
		labels = {'quantity': 'Quantity:'}

class SellForm(forms.ModelForm):
	class Meta:
		model = Asset
		fields = ['quantity']
		labels = {'quantity': 'Quantity:'}