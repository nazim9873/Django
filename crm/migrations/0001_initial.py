# Generated by Django 3.2.9 on 2021-12-06 10:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('course_id', models.AutoField(primary_key=True, serialize=False)),
                ('course_name', models.CharField(default='', max_length=50)),
                ('desc', models.CharField(default='', max_length=300)),
                ('course_date', models.DateField(default='')),
                ('price', models.IntegerField(default=0)),
                ('image', models.ImageField(default='', upload_to='crm/images')),
            ],
        ),
        migrations.CreateModel(
            name='Enquiry',
            fields=[
                ('enquiry_no', models.AutoField(primary_key=True, serialize=False)),
                ('ba_id', models.CharField(default='', max_length=50)),
                ('sources', models.CharField(default='', max_length=50)),
                ('student_firstname', models.CharField(default='', max_length=50)),
                ('student_lastname', models.CharField(default='', max_length=50)),
                ('email', models.EmailField(default='@gmail.com', max_length=100)),
                ('phone', models.IntegerField(default='')),
                ('course_name', models.CharField(default='', max_length=50)),
                ('qualifications', models.CharField(default='', max_length=100)),
                ('college', models.CharField(default='', max_length=100)),
                ('location', models.CharField(default='', max_length=100)),
                ('counsellor', models.CharField(default='', max_length=100)),
                ('demo_init', models.CharField(default='no', max_length=10)),
                ('trainer_name', models.CharField(default='no', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('registration_no', models.AutoField(primary_key=True, serialize=False)),
                ('student_firstname', models.CharField(default='', max_length=50)),
                ('student_lastname', models.CharField(default='', max_length=50)),
                ('email', models.EmailField(default='', max_length=100)),
                ('phone', models.IntegerField(default='')),
                ('father_name', models.CharField(default='', max_length=50)),
                ('father_phone', models.IntegerField()),
                ('perm_add', models.CharField(default='', max_length=200)),
                ('corres_add', models.CharField(max_length=100)),
                ('course_name', models.CharField(default='', max_length=50)),
                ('duration', models.CharField(default='', max_length=50)),
                ('registration_date', models.DateField()),
                ('ba_id', models.CharField(default='', max_length=50)),
                ('enroll_id', models.CharField(default='', max_length=50)),
                ('counsellor', models.CharField(default='', max_length=50)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='media/crm/photo')),
                ('aadhar_front', models.ImageField(blank=True, null=True, upload_to='media/crm/aadhar_front')),
                ('aadhar_back', models.ImageField(blank=True, null=True, upload_to='media/crm/aadhar_back')),
                ('total_fee', models.DecimalField(decimal_places=2, max_digits=10)),
                ('paid_fee', models.DecimalField(decimal_places=2, max_digits=10)),
                ('first_installment_amt', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('last_installment_date', models.DateField(null=True)),
                ('payment_date', models.DateField()),
                ('next_installment_date', models.DateField(null=True)),
                ('next_installment_amt', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('new_installment_amt', models.DecimalField(decimal_places=2, max_digits=10)),
                ('new_installment_date', models.DateField()),
                ('next_installment_amt', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('next_installment_date', models.DateField(null=True)),
                ('registration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.registration')),
            ],
            options={
                'ordering': ['new_installment_date'],
            },
        ),
        migrations.CreateModel(
            name='EnquiryFollowup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enquiry_desc', models.TextField()),
                ('pub_date', models.DateField(default='')),
                ('enquiry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.enquiry')),
            ],
            options={
                'ordering': ['pub_date'],
            },
        ),
    ]
