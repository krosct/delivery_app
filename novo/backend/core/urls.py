from django.urls import path, include

urlpatterns = [
    path('api/', include('modulos.delivery.http.urls')),
]
