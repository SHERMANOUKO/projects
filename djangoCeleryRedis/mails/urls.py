from django.conf.urls import url
from mails.views import CreateAccount

urlpatterns = [
    url(r'^createAccount', CreateAccount.as_view()),
]
