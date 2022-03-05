from django.urls import path
from django.views.generic import RedirectView

from otzovikapp.views.products import ProductsView, ProductCreate, ProductView, ProductUpdate, ProductDelete
from otzovikapp.views.reviews import ReviewCreate

app_name = 'otzovikapp'

urlpatterns = [
    path('', ProductsView.as_view(), name='index'),
    path('product/create/', ProductCreate.as_view(), name='product-create'),
    path('product/<int:pk>/', ProductView.as_view(), name='product-read'),
    path('product/<int:pk>/update/', ProductUpdate.as_view(), name='product-update'),
    path('product/<int:pk>/delete/', ProductDelete.as_view(), name='product-delete'),
    path('product/<int:pk>/review-create/', ReviewCreate.as_view(), name='review-create'),
]
