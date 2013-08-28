import urllib

from haystack.views import SearchView

class BaseSearchView(SearchView):
    def get_query(self):
        '''
        Returns query keywords provided by user and empty string if query
        is invalid.

        It also sets query_str to url encoded string of search values so it
        can be used for pagination (or empty string for invalid query).
        '''
        self.query_str = ""
        self.searched = False
        if self.form.is_valid():
            self.searched = True
            query_values = [ (key, value) for key, value in self.form.cleaned_data.items() if value or key == 'q' ]
            self.query_str = urllib.urlencode(query_values)
            return self.form.cleaned_data['q']
        return ''

    def get_results(self):
        '''
        Fetches the results via the form or returns an empty list if there's
        no query to search with.

        Valid queries have at least one form field in its request.
        '''
        query_keys = set(self.request.GET.keys())
        if self.form.is_valid():
            form_keys = set(self.form.cleaned_data.keys())
            if not form_keys.intersection(query_keys):
                self.searched = False
                return []
        return self.form.search()

    def extra_context(self):
        '''
        Adds extra context variables for search page.
        '''
        return {
            'query_string': self.query_str,
            'searched': self.searched
        }
