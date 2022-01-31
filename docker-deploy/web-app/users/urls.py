from django.urls import path
from . import views
from .views import NoneCompleteRideListView, ConfirmedRideListView, OpenRideListView, DriverConfirmedRideListView, \
    DriverOpenSearchRideListView, CompleteRideListView

app_name = 'users'

urlpatterns = [
    path('', views.home, name='home'),
    path('my_uncompleted_rides_list/', NoneCompleteRideListView.as_view(), name='my-uncompleted-rides-list'),
    path('my_completed_rides_list/', CompleteRideListView.as_view(), name='my-completed-rides-list'),
    path('my_open_rides_list/', OpenRideListView.as_view(), name='my-open-rides-list'),
    path('my_comfirmed_rides_list/', ConfirmedRideListView.as_view(), name='my-confirmed-rides-list'),
    path('open_share_ride_search/', views.openShareRideSearch, name='search-open-share-ride'),
    path('driver_comfirmed_rides_list/', DriverConfirmedRideListView.as_view(), name='driver-confirmed-rides-list'),
    path('driver_open_rides_list/', DriverOpenSearchRideListView.as_view(), name='driver-open-rides-list'),
]
