from django import forms

class SearchForm(forms.Form):
    SEARCH_CHOICES = (
        ('all', 'All'),
        ('name', 'Name'),
        ('nationality', 'Nationality'),
        ('club', 'Club')
    )
    q = forms.CharField(label="e.g. Messi, Argentina, or FC Barcelona", max_length=100, 
        widget=forms.TextInput(attrs={'class':'search-input'})
    )
    search_by = forms.ChoiceField(label="Search by:", widget=forms.RadioSelect(
        attrs={'class':'form-check-inline'}
    ), choices=SEARCH_CHOICES)

class TeamBuilderForm(forms.Form):
    budget = forms.IntegerField(label="e.g. 100000")