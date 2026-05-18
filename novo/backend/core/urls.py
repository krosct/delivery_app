from django.urls import path, include

urlpatterns = [
    path('api/v1/delivery/', include('modulos.delivery.http.urls')),
]
