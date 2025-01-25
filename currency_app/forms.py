import pytz
from django import forms


class CurrencyExchangeForm(forms.Form):
    amount = forms.DecimalField(
        label='Amount',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Sum'}),
    )

    from_currency = forms.ChoiceField(
        label='From',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    to_currency = forms.ChoiceField(
        label='To',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )


class CountryTimeForm(forms.Form):
    country = forms.CharField(
        label='Enter Continent/Country',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Example: Europe/London',
        })
    )