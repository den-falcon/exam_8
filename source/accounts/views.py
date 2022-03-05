from django.contrib.auth import login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from accounts.forms import MyUserCreationForm, PasswordChangeForm, UserChangeForm


# from accounts.models import Profile


class RegisterView(CreateView):
    model = User
    template_name = "registration.html"
    form_class = MyUserCreationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if not next_url:
            next_url = self.request.POST.get('next')
        if not next_url:
            next_url = reverse('otzovikapp:index')
        return next_url


class UserDetailView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'profile.html'
    context_object_name = 'user_obj'
    paginate_related_by = 5
    paginate_related_orphans = 0

    def get_context_data(self, **kwargs):
        reviews = self.object.reviews.order_by('-created_at')
        paginator = Paginator(reviews, self.paginate_related_by, orphans=self.paginate_related_orphans)
        page_number = self.request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        kwargs['page_obj'] = page
        kwargs['reviews'] = page.object_list
        kwargs['is_paginated'] = page.has_other_pages()
        return super().get_context_data(**kwargs)


# class AccountList(PermissionRequiredMixin, ListView):
#     model = get_user_model()
#     context_object_name = "users_obj"
#     template_name = "accounts_list.html"
#     paginate_by = 0
#     paginate_orphans = 0
#     permission_required = 'accounts.accounts_list'
#
#     def has_permission(self):
#         return super().has_permission()


class UserChangeView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = UserChangeForm
    template_name = 'user_change.html'
    context_object_name = 'user_obj'

    def get_object(self, queryset=None):
        return self.request.user
    #
    # def get_context_data(self, **kwargs):
    #     if 'profile_form' not in kwargs:
    #         kwargs['profile_form'] = self.get_profile_form()
    #     return super().get_context_data(**kwargs)
    #
    # def post(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     form = self.get_form()
    #     profile_form = self.get_profile_form()
    #     if form.is_valid() and profile_form.is_valid():
    #         return self.form_valid(form, profile_form)
    #     else:
    #         return self.form_invalid(form, profile_form)
    #
    # def form_valid(self, form, profile_form):
    #     response = super().form_valid(form)
    #     profile_form.save()
    #     return response
    #
    # def form_invalid(self, form, profile_form):
    #     context = self.get_context_data(form=form, profile_form=profile_form)
    #     return self.render_to_response(context)
    #
    # def get_profile_form(self):
    #     form_kwargs = {'instance': self.object.profile}
    #     if self.request.method == 'POST':
    #         form_kwargs['data'] = self.request.POST
    #         form_kwargs['files'] = self.request.FILES
    #     return ProfileChangeForm(**form_kwargs)

    def get_success_url(self):
        return reverse('accounts:profile', kwargs={'pk': self.object.pk})


class UserPasswordChangeView(UpdateView):
    model = get_user_model()
    template_name = 'user_password_change.html'
    form_class = PasswordChangeForm
    context_object_name = 'user_obj'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('accounts:login')
