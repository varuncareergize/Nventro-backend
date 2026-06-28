from django.urls import path
from .views import (
    VehicleServiceListView,
    VehicleServiceDetailView,
    ServiceDocumentListView,
    ServiceDocumentDetailView,
    ServicePartListView,
    ServicePartDetailView,
)

urlpatterns = [
    path('services/', VehicleServiceListView.as_view(), name='vehicle-service-list'),
    path('services/<int:pk>/', VehicleServiceDetailView.as_view(), name='vehicle-service-detail'),
    path('service-documents/', ServiceDocumentListView.as_view(), name='service-document-list'),
    path('service-documents/<int:pk>/', ServiceDocumentDetailView.as_view(), name='service-document-detail'),
    path('service-parts/', ServicePartListView.as_view(), name='service-part-list'),
    path('service-parts/<int:pk>/', ServicePartDetailView.as_view(), name='service-part-detail'),
]
