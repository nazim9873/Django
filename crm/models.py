from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=50, default="")
    desc = models.CharField(max_length=300, default="")
    course_date = models.DateField(default="")
    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to="crm/images", default="")

    def __str__(self):
        return self.course_name


class Enquiry(models.Model):
    enquiry_no = models.AutoField(primary_key=True)
    ba_id = models.CharField(max_length=50, default="")
    sources = models.CharField(max_length=50, default="")
    student_firstname = models.CharField(max_length=50, default="")
    student_lastname = models.CharField(max_length=50, default="")
    email = models.EmailField(max_length=100, default="@gmail.com")
    phone = models.IntegerField(default="")
    course_name = models.CharField(max_length=50, default="")
    qualifications = models.CharField(max_length=100, default="")
    college = models.CharField(max_length=100, default="")
    location = models.CharField(max_length=100, default="")
    counsellor = models.CharField(max_length=100, default="")
    demo_init = models.CharField(max_length=10, default="no")
    trainer_name = models.CharField(max_length=100, default="no")

    def __str__(self):
        return self.student_firstname

    def get_absolute_url(self):
        return "/enquiry_followup/%i/" % self.enquiry_no


class EnquiryFollowup(models.Model):
    enquiry_desc = models.TextField()
    pub_date = models.DateField(default="")
    enquiry = models.ForeignKey(Enquiry, on_delete=models.CASCADE)

    def __str__(self):
        return self.enquiry_desc

    class Meta:
        ordering = ['pub_date']


class Registration(models.Model):
    registration_no = models.AutoField(primary_key=True)
    student_firstname = models.CharField(max_length=50, default="")
    student_lastname = models.CharField(max_length=50, default="")
    email = models.EmailField(max_length=100, default="")
    phone = models.IntegerField(default="")
    father_name = models.CharField(max_length=50, default="")
    father_phone = models.IntegerField()
    perm_add = models.CharField(max_length=200, default="")
    corres_add = models.CharField(max_length=100)
    course_name = models.CharField(max_length=50, default="")
    duration = models.CharField(max_length=50, default="")
    registration_date = models.DateField()
    ba_id = models.CharField(max_length=50, default="")
    enroll_id = models.CharField(max_length=50, default="")
    counsellor = models.CharField(max_length=50, default="")
    photo = models.ImageField(null=True, blank=True, upload_to="media/crm/photo")
    aadhar_front = models.ImageField(null=True, blank=True, upload_to="media/crm/aadhar_front")
    aadhar_back = models.ImageField(null=True, blank=True, upload_to="media/crm/aadhar_back")
    total_fee = models.DecimalField(decimal_places=2, max_digits=10)
    paid_fee = models.DecimalField(decimal_places=2, max_digits=10)
    first_installment_amt = models.DecimalField(null=True, decimal_places=2, max_digits=10)
    last_installment_date = models.DateField(null=True)
    payment_date = models.DateField()
    next_installment_date = models.DateField(null=True)
    next_installment_amt = models.DecimalField(null=True, decimal_places=2, max_digits=10)

    def __str__(self):
        return self.student_firstname

    def get_absolute_url(self):
        return "/payment/%i/" % self.registration_no


class Payment(models.Model):
    new_installment_amt = models.DecimalField(decimal_places=2, max_digits=10)
    new_installment_date = models.DateField()
    next_installment_amt = models.DecimalField(null=True, decimal_places=2, max_digits=10)
    next_installment_date = models.DateField(null=True)
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.new_installment_date)

    class Meta:
        ordering = ['new_installment_date']
