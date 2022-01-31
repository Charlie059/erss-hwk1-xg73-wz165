from django.urls import path

import ride.views
from . import views
from .views import RideCreateView, RideDetailView, RideDeleteView, RideUpdateView, SharerUpdateView
app_name = 'ride'

urlpatterns = [
    path('new/', RideCreateView.as_view(), name='ride-create'),
    path('<int:pk>/', RideDetailView.as_view(), name='ride-detail'),
    path('<int:pk>/delete/', RideDeleteView.as_view(), name='ride-delete'),
    path('<int:pk>/update/', RideUpdateView.as_view(), name='ride-update'),
    path('<int:pk>/sharer_update/', ride.views.SharerUpdateView_test, name='ride-sharer-update'),
    path('<int:pk>/confirmed/', ride.views.confirm, name='ride-confirmed'),
    path('<int:pk>/completed/', ride.views.complete, name='ride-completed'),
    path('<int:pk>/join/', ride.views.join, name='ride-join'),
]
