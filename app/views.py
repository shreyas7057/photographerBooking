from django.shortcuts import redirect, render
from .models import Photographer,Category,Team,Gallery,Stat,Booking,Package,Service
from django.db.models import Q
from .forms import BookingForm
from django.conf import settings
from django.core.mail import send_mail

def index(request):
    query = request.GET.get('q','')
    if query:
        queryset = (Q(location__icontains=query))
        results = Photographer.objects.filter(queryset).distinct()
    else:
       results = Photographer.objects.all()
    context = {
        'results':results,
        'query':query,
    }
    return render(request,'index.html',context)


def visit_photography_site(request,id):
    photographer = Photographer.objects.get(id=id)

    gallery = Gallery.objects.filter(photographer=photographer.id)
    team = Team.objects.filter(photographer=photographer.id)
    stat = Stat.objects.get(photographer=photographer.id)
    package = Package.objects.filter(photographer=photographer.id)
    service = Service.objects.filter(photographer=photographer.id)

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
            return redirect('visit_photography_site',id=id)

    else:
        form = BookingForm()

    context = {
        'photographer':photographer,
        'gallery':gallery,
        'team':team,
        'stat':stat,
        'package':package,
        'service':service,
        'form':form,
    }
    return render(request,'app/home.html',context)
