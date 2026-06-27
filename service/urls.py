from django.urls import path
from .views import (
    VehicleServiceListView,
    VehicleServiceDetailView,
    ServiceItemListView,
    ServiceItemDetailView,
    VehicleServiceItemListView,
    VehicleServiceItemDetailView,
    ServiceDocumentListView,
    ServiceDocumentDetailView,
    PartListView,
    PartDetailView,
    ServicePartListView,
    ServicePartDetailView,
)

urlpatterns = [
    path('services/', VehicleServiceListView.as_view(), name='vehicle-service-list'),
    path('services/<int:pk>/', VehicleServiceDetailView.as_view(), name='vehicle-service-detail'),
    path('service-items/', ServiceItemListView.as_view(), name='service-item-list'),
    path('service-items/<int:pk>/', ServiceItemDetailView.as_view(), name='service-item-detail'),
    path('service-item-links/', VehicleServiceItemListView.as_view(), name='vehicle-service-item-list'),
    path('service-item-links/<int:pk>/', VehicleServiceItemDetailView.as_view(), name='vehicle-service-item-detail'),
    path('service-documents/', ServiceDocumentListView.as_view(), name='service-document-list'),
    path('service-documents/<int:pk>/', ServiceDocumentDetailView.as_view(), name='service-document-detail'),
    path('parts/', PartListView.as_view(), name='part-list'),
    path('parts/<int:pk>/', PartDetailView.as_view(), name='part-detail'),
    path('service-parts/', ServicePartListView.as_view(), name='service-part-list'),
    path('service-parts/<int:pk>/', ServicePartDetailView.as_view(), name='service-part-detail'),
]
