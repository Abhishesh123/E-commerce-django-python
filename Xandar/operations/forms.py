from django import forms
choices = [(i, str(i)) for i in range(1, 4)]


class UpdateCartForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=choices)