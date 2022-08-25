from django.urls import path

from django.contrib.auth import views as auth_views
from account_rest.views import SignUpForm, api_show_account, api_list_accounts, api_user_token, authenticate

urlpatterns = [
    path("login/", authenticate, name="login"),
    path("signup/", SignUpForm, name="signup"),
    path("accounts/", api_list_accounts, name="accounts_list"),
    path("accounts/<int:pk>", api_show_account, name="account_detail"),
    path("tokens/mine/", api_user_token, name="get_token")
]