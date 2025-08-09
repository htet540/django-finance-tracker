from django.urls import path
from . import views

app_name = "entities"

urlpatterns = [
    path("", views.entity_list, name="index"),
    path("add/", views.entity_create, name="add"),
    path("<int:pk>/edit/", views.entity_edit, name="edit"),
    path("<int:pk>/delete/", views.entity_delete, name="delete"),
    path("autocomplete/", views.entity_autocomplete, name="autocomplete"),
]