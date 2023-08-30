from django import forms


class SearchForm(forms.Form):
    fsearch_mag = forms.CharField(label='Magnitude:')
