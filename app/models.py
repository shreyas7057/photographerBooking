from django.db import models
from django.contrib.auth import get_user_model
import datetime

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Photographer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    studio_name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    cover_photo = models.ImageField(upload_to='cover_photos/',null=True,blank=True)
    your_photo = models.ImageField(upload_to='photographer_self/',blank=True,null=True)

    def __str__(self):
        return self.user.full_name



class Gallery(models.Model):
    photographer = models.ForeignKey(Photographer,on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='gallery')
    

    def __str__(self):
        return self.photographer.user.full_name


class Team(models.Model):
    photographer = models.ForeignKey(Photographer,on_delete=models.CASCADE)
    image = models.ImageField(upload_to="team/",blank=True,null=True)
    name = models.CharField(max_length=100)
    speciality = models.CharField(max_length=100)


    def __str__(self):
        return self.photographer.user.full_name



class Stat(models.Model):
    photographer = models.ForeignKey(Photographer,on_delete=models.CASCADE)
    projects = models.IntegerField()
    customers = models.IntegerField()
    albums = models.IntegerField()
    completed = models.IntegerField()

    def __str__(self):
        return self.photographer.user.full_name


class Service(models.Model):
    photographer = models.ForeignKey(Photographer,on_delete=models.CASCADE)
    serviceType = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.photographer.user.full_name



class Package(models.Model):
    photographer = models.ForeignKey(Photographer,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()

    def __str__(self):
        return self.photographer.user.full_name



class Booking(models.Model):

    BOOKING_STATUS = (
        ('Accepted','Accepted'),
        ('Rejected','Rejected'),
    )

    SHOOT_STATUS = (
        ("Not Started","Not Started"),
        ('Completed','Completed'),
    )

    photographer = models.ForeignKey(Photographer,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    mobile = models.CharField(max_length=10)
    start_date = models.DateField()
    end_date = models.DateField()
    address = models.TextField()
    no_of_days = models.IntegerField(null=True,blank=True)
    comment = models.TextField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)
        # f"{self.photographer.user.full_name} was booked by {self.name} on {self.start_date} till {self.end_date}"

    def save(self,*args,**kwargs):
        start_date = datetime.datetime.strptime(str(self.start_date), "%Y-%m-%d")
        end_date = datetime.datetime.strptime(str(self.end_date), "%Y-%m-%d")
        self.no_of_days = abs((end_date-start_date).days)
        return super().save(*args,**kwargs)

    
class Invoice(models.Model):
    photographer = models.ForeignKey(Photographer,on_delete=models.CASCADE)
    package = models.ForeignKey(Package,on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking,on_delete=models.CASCADE)
    extra_amt = models.IntegerField(null=True,blank=True)
    total_amt = models.IntegerField(null=True,blank=True)
    payment_status = models.CharField(max_length=100)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


    def __str__(self):
        return self.photographer.user.full_name

    
    def calc_total_amt(self):
        self.total_amt = self.package.price+self.extra_amt
        return self.total_amt
