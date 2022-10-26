from django.urls import path
from .views import ListProductView, TesteView


urlpatterns = [
    path("products/", ListProductView.as_view()),
    path("products/<pk>/", TesteView.as_view()),
]
