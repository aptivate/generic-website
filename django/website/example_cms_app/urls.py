from django.conf.urls.defaults import *
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from haystack.forms import ModelSearchForm
from haystack.query import SearchQuerySet
from haystack.views import SearchView, search_view_factory

from models import AnotherExampleModel
from forms import ExampleSearchForm
from views import ExampleSearchView

sqs = SearchQuerySet().models(AnotherExampleModel)

urlpatterns = patterns('',
    url(r'^$', csrf_exempt(search_view_factory(
        view_class=ExampleSearchView,
        template='sr_search.html',
        searchqueryset=sqs,
        form_class=ExampleSearchForm,
        results_per_page=15
        )), name='sr_search'),

    url(r'details/(?P<pk>\w+)/$',
        DetailView.as_view(template_name='sr_details.html', model=AnotherExampleModel),
        name='sr_details'),
)

