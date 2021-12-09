from django import forms
import datetime
from .models import *


class RegistrationForm(forms.ModelForm):
    registration_date = forms.DateField(initial=datetime.date.today, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    first_installment_amt = forms.DecimalField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    payment_date = forms.DateField(initial=datetime.date.today, help_text='First Installment', required=False,
                                   widget=forms.TextInput(
                                       attrs={'class': 'form-control'}))
    next_installment_amt = forms.DecimalField(label="Next Installment Amount", required=False, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    next_installment_date = forms.DateField(label="Next Installment Date", required=False, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    CHOICES_dur = (

        ('Select', 'Select'),
        ('6 months', '6 months'),
        ('2 months', '2 months'),
        ('others', 'others'),
    )
    CHOICES_coun = (
        ('Select', 'Select'),
        ('Aliya Khanna', 'Aliya Khanna'),
        ('Preeti Sharma', 'Preeti Sharma'),
        ('Pooja Desai', 'Pooja Desai'),
    )
    CHOICES_ba = (
        ('Select', 'Select'),
        ('001', '001'),
        ('002', '002'),
        ('003', '003'),
    )
    CHOICES_course = (
        ('Select', 'Select'),
        ('ML with Python', 'ML with Python'),
        ('FullStack Development', 'FullStack Development'),
        ('Robotics', 'Robotics'),
        ('IOT', 'IOT'),
        ('Data Science', 'Data Science'),
        ('Job Oriented Course-ML', 'Job Oriented Course-ML')
    )
    course_name = forms.ChoiceField(choices=CHOICES_course, widget=forms.Select(
        attrs={'class': 'form-control'}))
    duration = forms.ChoiceField(choices=CHOICES_dur, widget=forms.Select(
        attrs={'class': 'form-control'}))
    ba_id = forms.ChoiceField(choices=CHOICES_ba, widget=forms.Select(
        attrs={'class': 'form-control'}))
    counsellor = forms.ChoiceField(choices=CHOICES_coun, widget=forms.Select(
        attrs={'class': 'form-control'}))

    class Meta:
        model = Registration
        fields = ['student_firstname', 'student_lastname', 'email', 'phone', 'father_name', 'father_phone', 'perm_add',
                  'corres_add',
                  'course_name', 'duration', 'registration_date', 'ba_id', 'enroll_id', 'counsellor', 'photo',
                  'aadhar_front', 'aadhar_back',
                  'total_fee', 'first_installment_amt']
        labels = {'student_firstname': 'Name ', 'student_lastname': "   ", 'father_name': "Father's Name ",
                  'father_phone': "Father's Contact Number ",
                  'perm_add': "Permanent Address ", 'corres_add': "Corresponding Address ",
                  'ba_id': "Business Associate ID ",
                  'enroll_id': "Enrollment ID "}
        error_messages = {'student_firstname': {'required': ('Please enter your first name'), },
                          'student_lastname': {'required': ('Please enter your last name'), },
                          'email': {'required': ('Please enter email id'), },
                          'phone': {'required': ('Please enter your name'), },
                          'father_name': {'required': ("Please enter your father's name"), }}
        widgets = {'student_firstname': forms.TextInput(attrs={'class': 'form-control',
                                                               'placeholder': "Firstname"}),
                   'student_lastname': forms.TextInput(attrs={'class': 'form-control',
                                                              'placeholder': "Lastname"}),
                   'email': forms.EmailInput(attrs={'class': 'form-control',
                                                    'placeholder': ""}),
                   'phone': forms.TextInput(attrs={'class': 'form-control',
                                                   'placeholder': ""}),
                   'father_name': forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': ""}),
                   'father_phone': forms.TextInput(attrs={'class': 'form-control',
                                                          'placeholder': ""}),
                   'perm_add': forms.Textarea(attrs={'class': 'form-control', "rows": 5, "cols": 20,
                                                     'placeholder': ""}),
                   'corres_add': forms.Textarea(attrs={'class': 'form-control', "rows": 5, "cols": 20,
                                                       'placeholder': ""}),
                   'registration_date': forms.TextInput(attrs={'class': 'form-control',
                                                               'placeholder': ""}),
                   'enroll_id': forms.TextInput(attrs={'class': 'form-control',
                                                       'placeholder': ""}),
                   'total_fee': forms.TextInput(attrs={'class': 'form-control',
                                                       'placeholder': ""}),
                   'first_installment_amt': forms.TextInput(attrs={'class': 'form-control',
                                                                   'placeholder': ""}),
                   'photo': forms.FileInput(
                       attrs={'class': 'form-control form-control-sm'}),
                   'aadhar_front': forms.FileInput(
                       attrs={'class': 'form-control form-control-sm'}),
                   'aadhar_back': forms.FileInput(
                       attrs={'class': 'form-control form-control-sm'})

                   }

    def clean_first_installment_amt(self):
        first_installment_amt = self.cleaned_data['first_installment_amt']
        total_fee = self.cleaned_data['total_fee']
        if first_installment_amt > total_fee:
            raise forms.ValidationError("Invalid Amount")
        return first_installment_amt


class PaymentForm(forms.ModelForm):
    new_installment_amt = forms.DecimalField(label="New Installment Amount", widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    new_installment_date = forms.DateField(initial=datetime.date.today, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    next_installment_amt = forms.DecimalField(label="Next Installment Amount", required=False, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    next_installment_date = forms.DateField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    registration = forms.ModelChoiceField(queryset=Registration.objects.all(), required=False)

    class Meta:
        model = Payment
        fields = "__all__"
