from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views

app_name = "song"

urlpatterns = [
    path("api/v1/player/", views.index, name="index"),
]