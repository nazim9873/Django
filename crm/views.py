from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from .models import *
from django.db.models import Q, Sum
import json
from .forms import RegistrationForm, PaymentForm


# Create your views here.
def index(request):
    regs = Registration.objects.all()
    enquirys = Enquiry.objects.all()
    params = {'regs': regs, "enquirys": enquirys}
    return render(request, 'crm/index.html', params)


def enquiry(request):
    if request.method == 'POST':
        ba_id = request.POST['ba_id']
        source = request.POST['source']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        phone = request.POST['phone']
        course = request.POST['course']
        qual = request.POST['qual']
        college = request.POST['college']
        state = request.POST['state']
        counsellor = request.POST['counsellor']
        demo_init = request.POST.get("demo_init", 'No')
        trainer = request.POST['trainer']

        data = Enquiry(ba_id=ba_id, sources=source, student_firstname=firstname, student_lastname=lastname, email=email,
                       phone=phone,
                       course_name=course, qualifications=qual, college=college, location=state, counsellor=counsellor,
                       demo_init=demo_init, trainer_name=trainer)
        data.save()
        status = "Submitted Successfully"
        return render(request, 'crm/enquiry.html', {'status': status})

    return render(request, 'crm/enquiry.html')


def registration(request):
    if request.method == 'POST':
        r = RegistrationForm(request.POST, request.FILES)
        if r.is_valid():
            firstname = r.cleaned_data['student_firstname']
            lastname = r.cleaned_data['student_lastname']
            email = r.cleaned_data['email']
            phone = r.cleaned_data['phone']
            fathername = r.cleaned_data['father_name']
            fatherphone = r.cleaned_data['father_phone']
            perm = r.cleaned_data['perm_add']
            corres = r.cleaned_data['corres_add']
            course = r.cleaned_data['course_name']
            duration = r.cleaned_data['duration']
            reg_date = r.cleaned_data['registration_date']
            enroll = r.cleaned_data['enroll_id']
            ba_id = r.cleaned_data['ba_id']
            total_fee = r.cleaned_data['total_fee']
            first_installment_amt = r.cleaned_data['first_installment_amt']
            paid_fee = first_installment_amt
            payment_date = r.cleaned_data['payment_date']
            counsellor = r.cleaned_data['counsellor']
            last_installment_date = payment_date
            install_date = r.cleaned_data['next_installment_date']
            install_amt = r.cleaned_data['next_installment_amt']

            data = Registration(student_firstname=firstname, student_lastname=lastname, email=email,
                                phone=phone, father_name=fathername, father_phone=fatherphone, perm_add=perm,
                                corres_add=corres, course_name=course, duration=duration, registration_date=reg_date,
                                ba_id=ba_id, enroll_id=enroll, total_fee=total_fee, paid_fee=paid_fee,
                                next_installment_date=install_date, next_installment_amt=install_amt,
                                counsellor=counsellor, first_installment_amt=first_installment_amt,
                                payment_date=payment_date,
                                last_installment_date=last_installment_date)

            data.save()
            status = "Submitted Successfully"
            r = RegistrationForm()
            return render(request, 'crm/registration.html', {'status': status, "r_form": r})
        print(r.errors)
    else:
        r = RegistrationForm()
        return render(request,'crm/registration.html', {"r_form": r})


def services(request):
    return render(request, 'crm/services.html')


def enquiry_followup(request, pk):
    if request.method == 'POST':
        data = Enquiry.objects.get(enquiry_no=pk)
        enquiry_desc = request.POST['enquiry_desc']
        pub_date = request.POST['pub_date']
        data1 = EnquiryFollowup.objects.create(enquiry_desc=enquiry_desc, pub_date=pub_date, enquiry=data)
        data1.save()
        return redirect(request.path_info)
    data = Enquiry.objects.get(enquiry_no=pk)
    data2 = EnquiryFollowup.objects.filter(enquiry=data)
    data3 = data2.values("enquiry_desc", "pub_date")
    params = {"student_firstname": data.student_firstname, "student_lastname": data.student_lastname,
              "email": data.email, "enquiry_no": data.enquiry_no, "sources": data.sources,
              "phone": data.phone,
              "course_name": data.course_name, "trainer_name": data.trainer_name,
              "qualifications": data.qualifications,
              "ba_id": data.ba_id, "college": data.college, "location": data.location,
              "demo_init": data.demo_init,
              "counsellor": data.counsellor,
              "enqs": data3}
    return render(request, 'crm/enquiry_followup.html', params)


def details(request):
    if request.method == 'POST':
        from_date = request.POST['from']
        to_date = request.POST['to']
        start_date = datetime.fromisoformat(from_date)
        end_date = datetime.fromisoformat(to_date)
        bar_new = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        months = (end_date.year - start_date.year) * 12 + end_date.month - start_date.month

        for n in range(int(months)):
            m = 30 * n
            date = start_date + timedelta(days=m)
            new_students = Registration.objects.filter(payment_date__month=date.month, payment_date__year=date.year)
            print(date.month)
            new_students = new_students.aggregate(Sum('first_installment_amt'))
            new_students = new_students['first_installment_amt__sum']

            if new_students == None:
                bar_new[date.month] = 0
            else:
                bar_new[date.month - 1] = float(new_students)
        json_bar_new = json.dumps(bar_new)
        print("wewe", bar_new)
        bar_old = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for n in range(int(months)):
            date = start_date + timedelta(n)
            old_students = Payment.objects.filter(new_installment_date__month=date.month,
                                                  new_installment_date__year=date.year)
            old_students = old_students.aggregate(Sum('new_installment_amt'))
            old_students = old_students['new_installment_amt__sum']
            if old_students == None:
                bar_old[date.month] = 0
            else:
                bar_old[date.month - 1] = float(old_students)
        json_bar_old = json.dumps(bar_old)

        total_students = Registration.objects.filter(registration_date__range=[from_date, to_date])
        student_total = total_students.aggregate(Sum('total_fee'))
        student_paid = total_students.aggregate(Sum('paid_fee'))
        student_pending = float(student_total['total_fee__sum']) - float(student_paid['paid_fee__sum'])
        params = {
            "bar_new": json_bar_new, "bar_old": json_bar_old,

            "total_fee": student_total['total_fee__sum'],
            "pending_fee": student_pending, "paid_fee": student_paid['paid_fee__sum']
        }
        print(bar_new, bar_old, student_paid)
        return redirect(request.path_info, params)
    bar_new = []
    for i in range(1, 13):
        new_students = Registration.objects.filter(payment_date__month=i, payment_date__year=datetime.today().year)
        new_students = new_students.aggregate(Sum('first_installment_amt'))
        new_students = new_students['first_installment_amt__sum']
        if new_students == None:
            bar_new.append(0)
        else:
            new_students = int(new_students)
            bar_new.append(new_students)
    json_bar_new = json.dumps(bar_new)
    bar_old = []
    for i in range(1, 13):
        old_students = Payment.objects.filter(new_installment_date__month=i,
                                              new_installment_date__year=datetime.today().year)
        old_students = old_students.aggregate(Sum('new_installment_amt'))
        old_students = old_students['new_installment_amt__sum']
        if old_students == None:
            bar_old.append(0)
        else:
            old_students = int(old_students)
            bar_old.append(old_students)
    json_bar_old = json.dumps(bar_old)

    total_students = Registration.objects.filter(registration_date__year=datetime.today().year)
    student_total = total_students.aggregate(Sum('total_fee'))
    student_paid = total_students.aggregate(Sum('paid_fee'))
    student_pending = float(student_total['total_fee__sum']) - float(student_paid['paid_fee__sum'])

    params = {
        "bar_new": json_bar_new, "bar_old": json_bar_old,

        "total_fee": student_total['total_fee__sum'],
        "pending_fee": student_pending, "paid_fee": student_paid['paid_fee__sum']
    }

    return render(request, 'crm/details.html', params)


def enquiry_search(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        ba_id = request.POST['ba_id']
        source = request.POST['source']
        data = Enquiry.objects.get(
            Q(student_firstname__icontains=firstname) & Q(ba_id__icontains=ba_id) & Q(sources__icontains=source))
        data2 = EnquiryFollowup.objects.filter(enquiry=data)
        data3 = data2.values("enquiry_desc", "pub_date")
        return redirect(data, permanent=True)
    return render(request, 'crm/enquiry_search.html')


def payment_search(request):
    if request.method == 'POST':
        name = request.POST['name']
        name = name.lower()
        enroll = request.POST['enroll']
        data = Registration.objects.get(Q(student_firstname__iexact=name) & Q(enroll_id__iexact=enroll))
        print(data.email)
        return redirect(data, permanent=True)
    return render(request, 'crm/payment_search.html')


def payment(request, pk):
    p = PaymentForm()
    if request.method == 'POST':
        data = Registration.objects.get(registration_no=pk)
        p = PaymentForm(request.POST)
        if p.is_valid():
            new_installment_amt = p.cleaned_data['new_installment_amt']
            new_installment_date = p.cleaned_data['new_installment_date']
            next_installment_amt = p.cleaned_data['next_installment_amt']
            next_installment_date = p.cleaned_data['next_installment_date']
            data1 = Payment.objects.create(new_installment_amt=new_installment_amt,
                                           next_installment_amt=next_installment_amt,
                                           next_installment_date=next_installment_date,
                                           new_installment_date=new_installment_date,
                                           registration=data)
            data1.save()
            data.next_installment_amt = next_installment_amt
            data.next_installment_date = next_installment_date

            data.pending_fee = data.total_fee - data.paid_fee
            data.last_installment_date = new_installment_date
            data.save()
        print(p.errors)
        return redirect(request.path_info)
    data = Registration.objects.get(registration_no=pk)
    data2 = Payment.objects.filter(registration=data)
    count = Payment.objects.filter(registration=data).count()
    data3 = data2.values("new_installment_amt", "new_installment_date", "next_installment_amt", "next_installment_date")
    print(data3)
    total_pay = 0
    for i in range(0, count):
        total_pay = total_pay + data3[i]['new_installment_amt']
    print(total_pay)
    paid_fee = data.paid_fee + total_pay
    params = {"student_firstname": data.student_firstname, "student_lastname": data.student_lastname,
              "email": data.email,
              "phone": data.phone, "father_name": data.father_name, "father_phone": data.father_phone,
              "perm_add": data.perm_add,
              "corres_add": data.corres_add, "course_name": data.course_name, "duration": data.duration,
              "registration_date": data.registration_date,
              "ba_id": data.ba_id, "enroll_id": data.enroll_id, "total_fee": data.total_fee,
              "paid_fee": paid_fee,
              "next_installment_date": data.next_installment_date,
              "next_installment_amt": data.next_installment_amt,
              "counsellor": data.counsellor,
              "pays": data3, 'p_form': p}

    return render(request, 'crm/payment.html', params)
