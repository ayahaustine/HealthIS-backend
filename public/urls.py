from django.urls import path
from .views import PublicClientListView, PublicClientRetrieveView

urlpatterns = [
    path('clients/', PublicClientListView.as_view(), name='public-client-list'),
    path('clients/<str:uuid>/', PublicClientRetrieveView.as_view(), name='public-client-detail'),
]
