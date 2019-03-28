from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search, name="search"),
    path("mentions-legales/", views.legals),
    path("details/<id_product>", views.details, name="details"),
    path("save-substitute/", views.save_substitute, name="save_substitute"),
    path("my-products/", views.my_products, name="my_products")
]
