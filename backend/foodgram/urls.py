from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path('api/', include('api.urls', namespace='api')),
    # path('admin/', admin.site.urls),
]
