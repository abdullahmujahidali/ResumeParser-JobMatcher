from django.urls import include, path
from .views import UserView

from rest_framework.routers import DefaultRouter

user_router = DefaultRouter()

user_router.register(r"users", UserView, basename="users")


urlpatterns = [
    path('', include(user_router.urls))
]
