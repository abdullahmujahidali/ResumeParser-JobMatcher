from django.urls import include, path
from .views import AIAssistantViewSet

from rest_framework.routers import DefaultRouter

assistant_router = DefaultRouter()

assistant_router.register(
    r"assistant", AIAssistantViewSet, basename="aiassistant")


urlpatterns = [
    path('', include(assistant_router.urls))
]
