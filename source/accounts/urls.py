from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.views.generic import RedirectView

from accounts.views import RegisterView, UserDetailView, UserChangeView, UserPasswordChangeView

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(template_name="login.html"), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('registration/', RegisterView.as_view(), name="registration"),
    path('<int:pk>/', UserDetailView.as_view(), name='profile'),
    path('change/', UserChangeView.as_view(), name='account-change'),
    path('password-change/', UserPasswordChangeView.as_view(), name='password-change'),
]
