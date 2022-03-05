from django.core.paginator import Paginator
from django.db.models.aggregates import Avg
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from otzovikapp.forms import ProductForm
from otzovikapp.models import Product
from otzovikapp.views.base import SearchView


class ProductsView(SearchView):
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'products'
    ordering = ['name', 'category']
    paginate_by = 5
    search_fields = ['name__icontains', 'description__icontains']


class ProductView(DetailView):
    model = Product
    context_object_name = "product"
    template_name = 'products/read.html'
    paginate_related_by = 5
    paginate_related_orphans = 0

    def get_context_data(self, **kwargs):
        reviews = self.object.reviews.filter(is_moderated=True).order_by('-created_at')
        paginator = Paginator(reviews, self.paginate_related_by, orphans=self.paginate_related_orphans)
        page_number = self.request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        if reviews:
            print(reviews)
            kwargs['avg'] = reviews.aggregate(Avg('rating'))
        else:
            kwargs['avg'] = 0
        kwargs['page_obj'] = page
        kwargs['reviews'] = page.object_list
        kwargs['is_paginated'] = page.has_other_pages()
        return super().get_context_data(**kwargs)


class ProductCreate(CreateView):
    model = Product
    form_class = ProductForm
    template_name = "products/create.html"

    def get_success_url(self):
        return reverse('otzovikapp:product-read', kwargs={'pk': self.object.pk})


class ProductUpdate(UpdateView):
    model = Product
    template_name = 'products/update.html'
    form_class = ProductForm

    def get_success_url(self):
        return reverse("otzovikapp:product-read", kwargs={"pk": self.object.pk})


class ProductDelete(DeleteView):
    model = Product
    template_name = 'products/delete.html'
    success_url = reverse_lazy('otzovikapp:index')

