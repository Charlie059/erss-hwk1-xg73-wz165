from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.core.validators import MinValueValidator, MaxValueValidator
from django.forms import SelectDateWidget, DateTimeInput
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, FormView
from ride.models import Ride
from users.forms import ShareUpdateRideFrom


class RideCreateView(LoginRequiredMixin, CreateView):
    model = Ride
    fields = ['arrive_date', 'starting_location', 'destination', 'share', 'special_request', 'vehicle_type']

    def get_form(self, form_class=None):
        form = super(RideCreateView, self).get_form(form_class)
        form.fields['special_request'].required = False
        form.fields['arrive_date'].widget = DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'})
        return form

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


# TODO Tests SharerUpdateView
#     ride = Ride.objects.get(id=pk)
@login_required
def SharerUpdateView_test(request, pk):
    form = ShareUpdateRideFrom(request.POST)
    ride = Ride.objects.get(id=pk)
    if request.method == 'POST':
        if form.is_valid():
            # Check the form value
            num_Of_Sharer = form.cleaned_data.get('num_Of_Passenger')
            if 0 <= num_Of_Sharer - 1 <= ride.seat_available:
                ride.passenger_number += (num_Of_Sharer - 1)
                print(ride.passenger_number)
                print(ride.seat_available)
                messages.success(request, f'Update Passenger number successful!')
            else:
                messages.warning(request, f'Update Passenger number failure, you can only update once ! Please check your value!')
            ride.save()
    return render(request, 'ride/ride_sharer_update.html', {'form':form})

# @login_required
# def openShareRideSearch(request):
#     data = []
#     form = SearchShareRideFrom(request.POST)
#     if request.method == 'POST':
#         if form.is_valid():
#             destination = form.cleaned_data.get('destination')
#             earliest_arrive_time = form.cleaned_data.get('earliest_arrive_time')
#             latest_arrive_time = form.cleaned_data.get('latest_arrive_time')
#             numOfPassenger = form.cleaned_data.get('num_Of_Passenger')
#             data = Ride.objects.filter(Q(share=True) & Q(status="OPEN") &
#                                        Q(destination=destination) & Q(
#                 arrive_date__range=(earliest_arrive_time, latest_arrive_time)) &Q(seat_available__gte=numOfPassenger))
#     return render(request, 'ride/open_ride_search.html', {'form': form, "data": data})


class SharerUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ride
    fields = ['passenger_number']

    def form_valid(self, form):
        # form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        ride = self.get_object()
        if (self.request.user == ride.who_on_car.all().filter(
                id=self.request.user.id).first() and ride.status == 'OPEN'):
            return True
        return False

    def get_form(self, form_class=None):
        form = super(SharerUpdateView, self).get_form(form_class)

        ride = self.get_object()
        sharerNum = ride.who_on_car.count()
        carType = ride.vehicle_type
        if carType == 'X':
            canCarry = 3
        else:
            canCarry = 5

        form.fields['passenger_number'].validators = [MinValueValidator(sharerNum + 1), MaxValueValidator(canCarry)]
        return form


class RideUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ride
    fields = ['arrive_date', 'starting_location', 'destination', 'share', 'special_request', 'vehicle_type']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        ride = self.get_object()
        if (self.request.user == ride.owner and ride.status == 'OPEN'):
            return True
        return False


class RideDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Ride
    template_name = 'ride/ride_detail.html'

    def test_func(self):
        ride = self.get_object()
        if (self.request.user == ride.owner and ride.status != 'COMPLETED') or (
                self.request.user == ride.who_on_car.all().filter(
            id=self.request.user.id).first() and ride.status != 'COMPLETED') or (
                self.request.user.vehicle_type != "" and ride.status == 'OPEN') or (
                self.request.user.vehicle_type != "" and ride.driver == self.request.user) or (
                ride.share == True and ride.status == 'OPEN'):
            return True
        return False

    def checkSharerUpdateDetail(self):
        ride = self.get_object()
        if (self.request.user == ride.who_on_car.all().filter(
                id=self.request.user.id).first() and ride.status == 'OPEN'):
            return True
        return False

    def checkUserUpdateDetail(self):
        ride = self.get_object()
        if self.request.user == ride.owner and ride.status == 'OPEN':
            return True
        return False

    # TODO: check passage value
    def checkUserJoinRide(self):
        ride = self.get_object()
        if ride.status == 'OPEN' and ride.share == True and ride.owner != self.request.user and self.request.user != ride.who_on_car.all().filter(
                id=self.request.user.id).first():
            return True
        return False

    def checkDriverConfirmedButton(self):
        ride = self.get_object()
        if self.request.user.vehicle_type != "" and ride.status == 'OPEN':
            return True
        return False

    def checkDriverCompleteButton(self):
        ride = self.get_object()
        if ride.status == 'CONFIRMED' and ride.driver == self.request.user:
            return True
        return False

    def get(self, request, pk):
        res = self.test_func()
        checkUserUpdateDetail = self.checkUserUpdateDetail()
        checkDriverConfirmedButton = self.checkDriverConfirmedButton()
        checkUserJoinRide = self.checkUserJoinRide()
        checkDriverCompleteButton = self.checkDriverCompleteButton()
        checkSharerUpdateDetail = self.checkSharerUpdateDetail()

        ride = Ride.objects.get(id=pk)
        return render(request, 'ride/ride_detail.html',
                      {'res': res, 'object': ride, 'checkUserUpdateDetail': checkUserUpdateDetail,
                       'checkDriverConfirmedButton': checkDriverConfirmedButton, 'checkUserJoinRide': checkUserJoinRide
                          , 'checkDriverCompleteButton': checkDriverCompleteButton,
                       'checkSharerUpdateDetail': checkSharerUpdateDetail})


class RideDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ride
    success_url = '/'

    def test_func(self):
        ride = self.get_object()
        if self.request.user == ride.owner or ride.driver:
            return True
        return False


# TODO vaild
@login_required
def confirm(request, pk):
    ride = Ride.objects.get(id=pk)
    if ride.status == "OPEN" and request.user.vehicle_number != '' and ride.owner != request.user:
        ride.status = 'CONFIRMED'
        ride.driver = request.user
        ride.save()

        emailList = []
        for sharer in enumerate(ride.who_on_car.all()):
            emailList.append(sharer[1].email)
        send_mail(
            'Your ride has been confirmed',
            'Hi! ' + '\nPlease note that your ride to ' + ride.destination + ' at ' + ride.arrive_date.strftime(
                "%m/%d/%Y %H:%M:%S") + ' has been confirmed. \nYour driver is ' + ride.driver.username + '\nPlease check detail online, thank you!',
            'do_not_reply_ride_matser@outlook.com',
            [ride.owner.email] + emailList,
            fail_silently=False,
        )
        messages.success(request, f'Confirm Ride Successful. Email will send!')
    else:
        messages.warning(request, f'Cannot Confirm this ride, please check status!')
    return redirect('ride:ride-detail', pk)


# TODO number limits
@login_required
def join(request, pk):
    ride = Ride.objects.get(id=pk)
    carType = ride.vehicle_type
    if carType == 'X':
        canCarry = 3
    else:
        canCarry = 5

    if ride.status == "OPEN" and ride.share == True and canCarry >= ride.passenger_number + 1 and request.user != ride.owner:
        ride.who_on_car.add(request.user)
        ride.passenger_number = ride.passenger_number + 1
        messages.success(request, f'Join Ride Successful!')
        ride.save()
    else:
        messages.warning(request, f'Cannot join ride because it is not a share ride or open ride or it is max riders!')
    return redirect('ride:ride-sharer-update', pk)


@login_required
def complete(request, pk):
    ride = Ride.objects.get(id=pk)

    if ride.status == "CONFIRMED" and ride.driver == request.user:
        ride.status = 'COMPLETE'
        ride.save()
    else:
        messages.warning(request, f'Cannot complete ride because you are not driver!')
    return redirect('ride:ride-detail', pk)
