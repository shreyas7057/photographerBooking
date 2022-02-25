from django import forms
from .models import Booking,Package


class BookingForm(forms.ModelForm):
    class Meta:

        model = Booking
        fields = ['name','email','mobile','start_date','end_date','address','comment']

        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your name'}),
            'email':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your valid Email Address'}),
            'mobile':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your Mobile Number'}),
            'start_date':forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'end_date':forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'address':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter full Address'}),
            'comment':forms.Textarea(attrs={'class':'form-control','placeholder':'Comments/Requirements'}),
        }
        labels = {
            'start_date': ("Shoot Start Date:"),
            'end_date': ("Shoot End Date:"),
        }

    # def __init__(self, package, *args, **kwargs):
    #     super(BookingForm, self).__init__(*args, **kwargs)
    #     self.fields['package'].queryset = Booking.objects.filter(package__name=package)