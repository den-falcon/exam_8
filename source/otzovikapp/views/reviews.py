from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView

from otzovikapp.forms import ReviewForm
from otzovikapp.models import Review, Product


# PermissionRequiredMixin
class ReviewCreate(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'products/create.html'
    # permission_required = 'tracker_app.add_task'

    # def has_permission(self):
    #     return super().has_permission() and self.request.user in self.get_object().project.users.all()

    def form_valid(self, form):
        product = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        author = self.request.user
        review = form.save(commit=False)
        review.product = product
        review.author = author
        review.save()
        return redirect('otzovikapp:product-read', pk=product.pk)
