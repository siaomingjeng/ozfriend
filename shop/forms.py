from django import forms


class QuickSearch(forms.Form):
    chinese = forms.CharField(max_length=50, widget=forms.TextInput(
            attrs={'class': 'search_ME', 'id': 'search-text'}))
