from django.urls import path

from accounts.views import token_view

urlpatterns = [
    path("auth/token/", token_view, name="auth-token"),
]

