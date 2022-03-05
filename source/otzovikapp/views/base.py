from django.db.models import Q
from django.views.generic import ListView

from otzovikapp.forms import SearchForm


class SearchView(ListView):
    search_form_class = SearchForm
    search_form_field = "search"
    search_fields = []
    search_value = None
    form = None

    def get_queryset(self):
        self.form = self.get_form()
        self.search_value = self.get_search_value()
        queryset = super().get_queryset()
        if self.search_value:
            query = self.get_query()
            queryset = queryset.filter(query)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = SearchForm()
        if self.search_value:
            context['form'] = SearchForm(initial={self.search_form_field: self.search_value})
            context[self.search_form_field] = self.search_value
        return context

    def get_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get(self.search_form_field)

    def get_query(self):
        query = Q()
        for field in self.search_fields:
            kwargs = {field: self.search_value}
            query = query | Q(**kwargs)
        return query
