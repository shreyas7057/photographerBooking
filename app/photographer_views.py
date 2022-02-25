from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.contrib import messages
from .models import Booking,Package,Photographer,Service,Stat,Team,Gallery,Invoice
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from .forms import BookingForm
from django.conf import settings
from django.core.mail import send_mail

import csv
import xlwt

from io import StringIO, BytesIO
from xhtml2pdf import pisa
from django.utils.html import escape
from django.template.loader import get_template
from django.template import Context

User = get_user_model()



@login_required(login_url='login-user')
def custom_photographer_index(request):
    logged_in_user = request.user.id
    # photographer = Photographer.objects.get(user=logged_in_user)
    bookings = Booking.objects.filter(photographer__user=logged_in_user).count()
    todays_bookings = Booking.objects.all()
    # all_bookings = Booking.objects.filter(photographer=photographer)
    # incomplete_bookings = Booking.objects.filter(completed=False,photographer=photographer)

    
    # booking = Booking.objects.filter(
    #     photographer = photographer
    # )

    context = {
        'bookings':bookings,
        'todays_bookings':todays_bookings,
        # 'all_bookings':all_bookings,
        # 'incomplete_bookings':incomplete_bookings,
    }
    return render(request,'customadmin/photographer/photo_index.html',context)


@login_required(login_url='login-user')
def add_photographer_info(request):
    if request.method == 'POST':
        try:
            location = request.POST.get('location')
            studio_name = request.POST.get('studio_name')
            mobile = request.POST.get('mobile')
            address = request.POST.get('address')
            cover_photo = request.FILES.get('cover_photo')
            your_photo = request.FILES.get('your_photo')
            
            photographer = Photographer.objects.create(
                user = request.user,
                location=location,
                studio_name=studio_name,
                mobile = mobile,
                address = address,
                cover_photo = cover_photo,
                your_photo = your_photo,
            )
            photographer.save()
            messages.success(request,'Information Added Successfully!!!')
            return redirect('custom_photographer_index')
        except:
            messages.error(request,'You cannot same information twice!!!')
            return redirect('add_photographer_info')

    return render(request,'customadmin/photographer/add_photographer_info.html')


@login_required(login_url='login-user')
def view_photographer_info(request):
    photographer = Photographer.objects.get(
        user=request.user.id
    )
    context = {
        'photographer':photographer,
    }
    return render(request,'customadmin/photographer/view_photographer_info.html',context)


# edit link is created
def edit_photographer_info(request):
    photographer = Photographer.objects.get(
        user=request.user.id
    )
    context = {
        'photographer':photographer,
    }
    return render(request,'customadmin/photographer/edit_photographer_info.html',context)


# this functions edit the photographer information
def update_photographer_info(request):
    if request.method == "POSt":

        location = request.POST.get('location')
        studio_name = request.POST.get('studio_name')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        cover_photo = request.FILES.get('cover_photo')
        your_photo = request.FILES.get('your_photo')

        photographer = Photographer.objects.get(user=request.user.id)
        photographer.user = request.user
        photographer.location = location
        photographer.studio_name = studio_name
        photographer.mobile = mobile
        photographer.address = address
        photographer.cover_photo = cover_photo
        photographer.your_photo = your_photo


        if cover_photo != None and cover_photo != '':
            photographer.cover_photo = cover_photo

        if your_photo != None and your_photo != '':
            photographer.your_photo = your_photo

        photographer.save()
        messages.success(request,'Photographer information updated')
        return redirect('view_photographer_info')

    return render(request,'customadmin/photographer/edit_photographer_info.html')


@login_required(login_url='login-user')
def stat_add(request):
    if request.method == "POST":
        print("1")
        photographer =  Photographer.objects.get(user=request.user)
        try:
            projects = request.POST.get('projects')
            customers = request.POST.get('customers')
            albums = request.POST.get('albums')
            completed = request.POST.get('completed')
            stat = Stat.objects.create(
                photographer = photographer,
                projects = projects,
                customers = customers,
                albums = albums,
                completed = completed
            )
            stat.save()
            print("3")
            messages.success(request,'Stats added Successfull!!')
            return redirect('custom_photographer_index')
        except:
            print("4")
            messages.error(request,'You cannot same information twice!!!')
            return redirect('stat_add')

    return render(request,'customadmin/photographer/add_stat.html')


@login_required(login_url='login-user')
def view_stat(request):
    photographer = Photographer.objects.get(user=request.user)

    stat = Stat.objects.get(photographer=photographer)
    context = {
        'stat':stat,
    }
    return render(request,'customadmin/photographer/view_stat.html',context)


@login_required(login_url='login-user')
def add_gallery(request):
    photographer = Photographer.objects.get(user=request.user)
    if request.method == "POST":
        photo = request.FILES.get('photo')

        gallery = Gallery.objects.create(
            photographer = photographer,
            photo = photo,
        )
        gallery.save()
        messages.success(request,'Image Added Successfully')
        return redirect('view_gallery')
    
    return render(request,'customadmin/photographer/add_gallery.html')


@login_required(login_url='login-user')
def view_gallery(request):
    photographer = Photographer.objects.get(user=request.user)
    gallery = Gallery.objects.filter(
        photographer = photographer
    )
    context = {
        'gallery':gallery,
    }
    return render(request,'customadmin/photographer/view_gallery.html',context)


@login_required(login_url='login-user')
def add_team(request):
    photographer = Photographer.objects.get(user=request.user)
    if request.method == "POST":
        image = request.FILES.get('image')
        name = request.POST.get('name')
        speciality = request.POST.get('speciality')

        team = Team.objects.create(
            photographer = photographer,
            image = image,
            name = name,
            speciality = speciality
        )
        team.save()
        messages.success(request,'Team member added successfully')
        return redirect('view_team')
    
    return render(request,'customadmin/photographer/add_team.html')


@login_required(login_url='login-user')
def view_team(request):
    photographer = Photographer.objects.get(user=request.user)
    team = Team.objects.filter(
        photographer = photographer
    )
    context = {
        'team':team,
    }
    return render(request,'customadmin/photographer/view_team.html',context)


@login_required(login_url='login-user')
def delete_team(request,id):
    team = Team.objects.get(id=id)
    team.delete()
    messages.success(request,'Team deleted successfully!!!')
    return redirect('view_team')


@login_required(login_url='login-user')
def add_service(request):
    photographer = Photographer.objects.get(user=request.user)
    if request.method == "POST":
        serviceType = request.POST.get('serviceType')
        description = request.POST.get('description')

        service = Service.objects.create(
            photographer = photographer,
            serviceType = serviceType,
            description = description
        )
        service.save()
        messages.success(request,'Service Added Successfully!!')
        return redirect('view_service')
    
    return render(request,'customadmin/photographer/add_service.html')


@login_required(login_url='login-user')
def view_service(request):
    photographer = Photographer.objects.get(user=request.user)
    service = Service.objects.filter(
        photographer = photographer
    )
    context = {
        'service':service,
    }
    return render(request,'customadmin/photographer/view_service.html',context)


@login_required(login_url='login-user')
def delete_service(request,id):
    service = Service.objects.get(id=id)
    service.delete()
    messages.success(request,'Service deleted successfully!!!')
    return redirect('view_service')


@login_required(login_url='login-user')
def add_package(request):
    photographer = Photographer.objects.get(user=request.user)
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')

        package = Package.objects.create(
            photographer = photographer,
            name = name,
            description = description,
            price = price
        )
        package.save()
        messages.success(request,'Package added successfully!!')
        return redirect('view_package')
    
    return render(request,'customadmin/photographer/add_package.html')



@login_required(login_url='login-user')
def view_package(request):
    photographer = Photographer.objects.get(user=request.user)
    package = Package.objects.filter(
        photographer = photographer
    )
    context = {
        'package':package,
    }
    return render(request,'customadmin/photographer/view_package.html',context)


@login_required(login_url='login-user')
def delete_package(request,id):
    package = Package.objects.get(id=id)
    package.delete()
    messages.success(request,'Package deleted successfully!!!')
    return redirect('view_package')



@login_required(login_url='login-user')
def view_booking(request):
    photographer = Photographer.objects.get(user=request.user)
    booking = Booking.objects.filter(
        photographer = photographer
    )
    context = {
        'booking':booking,
    }
    return render(request,'customadmin/photographer/view_booking.html',context)


@login_required(login_url='login-user')
def add_booking(request):
    photographer = Photographer.objects.get(user=request.user)

    # booking form
    
    if request.method == "POST":

        form = BookingForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.photographer = photographer
            book.save()

            # send mail
            subject = "Booking Done!"
            content = "Name: "+book.name+" Shoot Start Date: "+str(book.start_date)+" till "+str(book.end_date)+" Number Of Days: "+str(book.no_of_days)
            tomail = book.email
            email_from = settings.EMAIL_HOST_USER
            send_mail(subject,content,email_from,[tomail,email_from,photographer.user.email],fail_silently=False,)
            return redirect('view_booking')

    else:
        form = BookingForm()

    context = {
        'photographer':photographer,
        'form':form,
    }
    return render(request,'customadmin/photographer/add_booking.html',context)


@login_required(login_url='login-user')
def delete_booking(request,id):
    booking = Booking.objects.get(id=id)
    booking.delete()
    messages.success(request,'Booking deleted successfully!!!')
    return redirect('view_booking')


@login_required(login_url='login-user')
def export_booking_csv(request):
    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="booking.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name','Email','Mobile','Start Date','End Date', 'Address','No. of Days','Comment','Completed','Created At'])

    photographer = Photographer.objects.get(user=request.user)
    booking = Booking.objects.filter(photographer=photographer).values_list('name','email','mobile','start_date','end_date','address','no_of_days','comment','completed','created_at')

    for hr in booking:
        writer.writerow(hr)
    return response


@login_required(login_url='login-user')
def export_booking_pdf(request):
    photographer = Photographer.objects.get(user=request.user)
    booking = Booking.objects.filter(photographer=photographer)
    data = {'booking':booking,'photographer':photographer,}
    template=get_template("customadmin/photographer/pdf_booking.html")
    data_p = template.render(data)
    response = BytesIO()

    pdfPage=pisa.pisaDocument(BytesIO(data_p.encode("UTF-8")),response)

    if not pdfPage.err:
        return HttpResponse(response.getvalue(),content_type="application/pdf")
    else:
        return HttpResponse("Error Generating PDF")


@login_required(login_url='login-user')
def generate_invoice(request,id):
    photographer = Photographer.objects.get(user=request.user)
    booking = Booking.objects.get(id=id)
    packages = Package.objects.filter(photographer=photographer)

    if request.method == "POST":
        package_get = request.POST.get('package')
        extra_amt = request.POST.get('extra_amt')
        payment_status = request.POST.get('payment_status')

        invoice = Invoice(
            photographer = photographer,
            booking = booking,
            package_id = package_get,
            extra_amt = extra_amt,
            payment_status = payment_status,
        )

        invoice.save()
        messages.success(request,'Invoice generated Successfully')
        return redirect('get_invoice')

    
    context = {
        'package':packages,
    }
    return render(request,'customadmin/photographer/generate_invoice.html',context)


@login_required(login_url='login-user')
def get_invoice(request):
    photographer = Photographer.objects.get(user=request.user)
    invoices = Invoice.objects.filter(photographer=photographer)
    context = {
        'invoices':invoices,
    }
    return render(request,'customadmin/photographer/all_invoices.html',context)


@login_required(login_url='login-user')
def download_invoice_pdf(request,id):
    invoice = Invoice.objects.get(id=id)
    data = {'invoice':invoice,}
    template=get_template("customadmin/photographer/download_invoice_pdf.html")
    data_p = template.render(data)
    response = BytesIO()

    pdfPage=pisa.pisaDocument(BytesIO(data_p.encode("UTF-8")),response)

    if not pdfPage.err:
        return HttpResponse(response.getvalue(),content_type="application/pdf")
    else:
        return HttpResponse("Error Generating PDF")