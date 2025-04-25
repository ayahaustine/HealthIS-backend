from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # API endpoints v1
    path('api/v1/accounts/', include('accounts.urls')),
    path('api/v1/programs/', include('programs.urls')),
    path('api/v1/clients/', include('clients.urls')),
    path('api/v1/enrollments/', include('enrollments.urls')),
]
