from django.urls import path
from .views import PartListView, PartDetailView, PartUsageListView, PartTransactionListView

urlpatterns = [
    path('', PartListView.as_view(), name='part-list'),
    path('<int:pk>/', PartDetailView.as_view(), name='part-detail'),
    path('usage/', PartUsageListView.as_view(), name='part-usage-list'),
    path('transactions/', PartTransactionListView.as_view(), name='part-transaction-list'),
]