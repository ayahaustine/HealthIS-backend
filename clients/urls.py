from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClientViewSet
router = DefaultRouter()
router.register(r'clients', ClientViewSet, basename='client')

urlpatterns = [
    path('', include(router.urls)),
    # path('<str:client_id>/programs/', ClientProgramsView.as_view(), name='client-programs'),

]