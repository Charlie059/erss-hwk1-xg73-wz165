from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import ListView
from ride.models import Ride

from .forms import Become2DriverForm, UserRegisterForm, ProfileUpdateForm, SearchShareRideFrom


def home(request):
    return redirect("login")


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'You Account has been activated!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def update_to_driver(request):
    if request.method == 'POST':
        u_form = Become2DriverForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'You Account has been updated!')
            return redirect('update_to_driver')
    else:
        u_form = Become2DriverForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, f'You Account has been updated!')
            return redirect('profile')
    else:
        p_form = ProfileUpdateForm(instance=request.user)

    context = {
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)


class NoneCompleteRideListView(ListView, LoginRequiredMixin):
    model = Ride
    template_name = 'users/rideList.html'
    context_object_name = 'rides'

    def get_queryset(self):
        return Ride.objects.filter((Q(owner=self.request.user) & (Q(status="OPEN") | Q(status="CONFIRMED"))) |
                                   (Q(who_on_car=self.request.user) & (Q(status="OPEN") |
                                                                       Q(status="CONFIRMED")))).order_by('arrive_date')

class CompleteRideListView(ListView, LoginRequiredMixin):
    model = Ride
    template_name = 'users/rideList.html'
    context_object_name = 'rides'

    def get_queryset(self):
        return Ride.objects.filter((Q(owner=self.request.user) & (Q(status="COMPLETE"))) |
                                   (Q(who_on_car=self.request.user) & (Q(status="COMPLETE")
                                                                       ))).order_by('arrive_date')


class OpenRideListView(ListView):
    model = Ride
    template_name = 'users/rideList.html'
    context_object_name = 'rides'

    def get_queryset(self):
        return Ride.objects.filter(Q(owner=self.request.user) & (Q(status="OPEN")))


class ConfirmedRideListView(ListView, LoginRequiredMixin):
    model = Ride
    template_name = 'users/rideList.html'
    context_object_name = 'rides'

    def get_queryset(self):
        return Ride.objects.filter(Q(owner=self.request.user) & (Q(status="CONFIRMED")))


class DriverConfirmedRideListView(ListView, LoginRequiredMixin):
    model = Ride
    template_name = 'users/rideList.html'
    context_object_name = 'rides'

    def get_queryset(self):
        return Ride.objects.filter(Q(driver=self.request.user) & (Q(status="CONFIRMED")))


class DriverOpenSearchRideListView(ListView, LoginRequiredMixin):
    model = Ride
    template_name = 'users/rideList.html'
    context_object_name = 'rides'

    # TODO Special info
    def get_queryset(self):
        special_info = self.request.user.special_info
        return Ride.objects.filter((Q(status="OPEN") & Q(vehicle_type=self.request.user.vehicle_type) & (
                    Q(special_request__icontains=special_info) | Q(special_request=''))))



@login_required
def openShareRideSearch(request):
    data = []
    form = SearchShareRideFrom(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            destination = form.cleaned_data.get('destination')
            earliest_arrive_time = form.cleaned_data.get('earliest_arrive_time')
            latest_arrive_time = form.cleaned_data.get('latest_arrive_time')
            numOfPassenger = form.cleaned_data.get('num_Of_Passenger')
            data = Ride.objects.filter(Q(share=True) & Q(status="OPEN") &
                                       Q(destination=destination) & Q(
                arrive_date__range=(earliest_arrive_time, latest_arrive_time)) &Q(seat_available__gte=numOfPassenger))
    return render(request, 'ride/open_ride_search.html', {'form': form, "data": data})
