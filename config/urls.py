from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # API endpoints v1
    path('api/v1/', include('accounts.urls')),
    path('api/v1/', include('programs.urls')),
    path('api/v1/', include('clients.urls')),
    path('api/v1/', include('enrollments.urls')),
    path('api/v1/public/', include('public.urls')),
    path('api/v1/analytics/', include('analytics.urls')),
]
