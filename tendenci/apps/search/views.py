from django.conf import settings
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404
from django.utils.translation import gettext_lazy as _

from tendenci.apps.theme.shortcuts import themed_response as render_to_resp
from tendenci.apps.search.forms import ModelSearchForm
from tendenci.apps.event_logs.models import EventLog

RESULTS_PER_PAGE = getattr(settings, 'HAYSTACK_SEARCH_RESULTS_PER_PAGE', 20)


def open_search(request, template_name="search/open_search_xml.html"):
    return render_to_resp(request=request, template_name=template_name,
        content_type="application/opensearchdescription+xml"
    )


class SearchView(object):
    template = 'search/search.html'
    extra_context = {}
    query = ''
    results = []
    request = None
    form = None

    def __init__(self, template=None, load_all=False, form_class=ModelSearchForm, searchqueryset=None):
        self.__qualname__ = self.__class__.__name__  # https://code.djangoproject.com/ticket/29296
        self.load_all = load_all
        self.form_class = form_class
        self.searchqueryset = searchqueryset
        self.user = None
        if template:
            self.template = template

    def __call__(self, request):
        """
        Generates the actual response to the search.

        Relies on internal, overridable methods to construct the response.
        """
        self.request = request
        self.user = self.request.user # to check for permissions

        self.form = self.build_form()
        self.query = self.get_query()
        self.results = self.get_results()
        # log an event
        EventLog.objects.log(action='global_search')

        return self.create_response(request)

    def build_form(self):
        """
        Instantiates the form the class should use to process the search query.
        """
        if self.searchqueryset is None:
            return self.form_class(self.request.GET, load_all=self.load_all, user=self.user)

        return self.form_class(self.request.GET, searchqueryset=self.searchqueryset, load_all=self.load_all, user=self.user)

    def get_query(self):
        """
        Returns the query provided by the user.

        Returns an empty string if the query is invalid.
        """
        if self.form.is_valid():
            return self.form.cleaned_data['q']

        return ''

    def get_results(self):
        """
        Fetches the results via the form.

        Returns an empty list if there's no query to search with.
        """
        if self.query:
            return self.form.search()

        return self.form.search(order_by='newest')

    def build_page(self):
        """
        Paginates the results appropriately.

        In case someone does not want to use Django's built-in pagination, it
        should be a simple matter to override this method to do what they would
        like.
        """
        paginator = Paginator(self.results, RESULTS_PER_PAGE)

        try:
            page = paginator.page(self.request.GET.get('page', 1))
        except InvalidPage:
            raise Http404

        return (paginator, page)

    def extra_context(self):
        """
        Allows the addition of more context variables as needed.

        Must return a dictionary.
        """
        # TODO: Add the selected models so they can be shown in the H1
        return {}

    def create_response(self, request):
        """
        Generates the actual HttpResponse to send back to the user.
        """
        (paginator, page) = self.build_page()

        context = {
            'query': self.query,
            'form': self.form,
            'ppage': page,
            'paginator': paginator,
        }
        context.update(self.extra_context())

        return render_to_resp(request=request, template_name=self.template, context=context)


class FacetedSearchView(SearchView):
    def __name__(self):
        return "FacetedSearchView"

    def extra_context(self):
        extra = super(FacetedSearchView, self).extra_context()

        if self.results == []:
            extra['facets'] = self.form.search().facet_counts()
        else:
            extra['facets'] = self.results.facet_counts()

        return extra


def basic_search(request, template='search/search.html', load_all=True, form_class=ModelSearchForm, searchqueryset=None, extra_context=None):
    """
    A more traditional view that also demonstrate an alternative
    way to use Haystack.

    Useful as an example of for basing heavily custom views off of.

    Also has the benefit of thread-safety, which the ``SearchView`` class may
    not be.

    Template:: ``search/search.html``
    Context::
        * form
          An instance of the ``form_class``. (default: ``ModelSearchForm``)
        * page
          The current page of search results.
        * paginator
          A paginator instance for the results.
        * query
          The query received by the form.
    """
    query = ''
    results = []

    if request.GET.get('q'):
        form = form_class(request.GET, searchqueryset=searchqueryset, load_all=load_all)

        if form.is_valid():
            query = form.cleaned_data['q']
            results = form.search()
    else:
        form = form_class(searchqueryset=searchqueryset, load_all=load_all)

    paginator = Paginator(results, RESULTS_PER_PAGE)

    try:
        page = paginator.page(int(request.GET.get('page', 1)))
    except InvalidPage:
        raise Http404(_("No such page of results!"))

    context = {
        'form': form,
        'page': page,
        'paginator': paginator,
        'query': query,
    }

    if extra_context:
        context.update(extra_context)

    return render_to_resp(request=request, template_name=template, context=context)
