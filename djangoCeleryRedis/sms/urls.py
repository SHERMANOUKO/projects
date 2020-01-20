from django.conf.urls import url
from sms.views import ScheduleDispatchSms

urlpatterns = [
    url(r'^dispatchSms', ScheduleDispatchSms.as_view()),
]