from django import forms

from models import ExampleModel
from haystack.forms import SearchForm
    
def get_choices(model, field):
    return [ ("", "all...") ] + [ (getattr(x, field), getattr(x, field)) for x in model.objects.all() ]

class ExampleSearchForm(SearchForm):
    q = forms.CharField(max_length=128, required=False, widget=forms.TextInput(attrs={'class': 'search_input'}))
    title = forms.CharField(max_length=500, required=False)
    author = forms.CharField(max_length=500, required=False)
    region = forms.CharField(max_length=255, required=False, widget=forms.Select(choices=get_choices(ExampleModel, 'name')))

    def search(self):
        # First, store the SearchQuerySet received from other processing.
        sqs = super(ExampleSearchForm, self).search()

        if hasattr(self, 'cleaned_data'):
            if not self.cleaned_data.get('q'): # Haystack gives up if no keywords, we don't
                sqs = self.searchqueryset
            if self.cleaned_data['title']:
                sqs = sqs.filter(title__in=[self.cleaned_data['title']])
            if self.cleaned_data['author']:
                sqs = sqs.filter(author__in=[self.cleaned_data['author']])
            if self.cleaned_data['region']:
                sqs = sqs.filter(region=self.cleaned_data['region'])

        return sqs
