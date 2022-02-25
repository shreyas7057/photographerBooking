from django.contrib.auth import get_user_model
from .models import Booking,Category,Package,Photographer,Service,Stat,Team,Gallery
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now


@login_required(login_url='login-user')
def custom_admin_index(request):
    photographers = Photographer.objects.all().count()
    bookings = Booking.objects.all().count()
    todays_booking = Booking.objects.filter(created_at=now()).count()
    photographer = Photographer.objects.all()

    context = {
        'photographers':photographers,
        'bookings':bookings,
        'todays_booking':todays_booking,
        'photographer':photographer,
    }
    return render(request,'customadmin/index.html',context)


