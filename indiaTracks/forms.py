from django import forms

class NameForm(forms.Form):
    districtName = forms.CharField(label='District Name', max_length=100)
