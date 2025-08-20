# reservation/forms.py
from django import forms

class BulkPriceForm(forms.Form):
    start_date = forms.DateField(widget=forms.SelectDateWidget)
    end_date = forms.DateField(widget=forms.SelectDateWidget)
    price = forms.DecimalField(max_digits=10, decimal_places=2)
