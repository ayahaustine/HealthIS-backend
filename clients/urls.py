from django.urls import path
from clients.views import (
    ClientCreateView,
    ClientListView,
    ClientRetrieveView,
    ClientUpdateView,
    ClientDeleteView,
)

urlpatterns = [
    path('clients/', ClientListView.as_view(), name='client-list'),
    path('clients/create/', ClientCreateView.as_view(), name='client-create'),
    path('clients/<str:uuid>/', ClientRetrieveView.as_view(), name='client-retrieve'),
    path('clients/<str:uuid>/update/', ClientUpdateView.as_view(), name='client-update'),
    path('clients/<str:uuid>/delete/', ClientDeleteView.as_view(), name='client-delete'),
]
