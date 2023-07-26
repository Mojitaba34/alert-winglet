from django.urls import path

from .views import TestView

app_name = "test_url"
urlpatterns = [path("test-url", TestView.as_view(), name="TESTING_API")]
