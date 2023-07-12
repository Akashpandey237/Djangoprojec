from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from .models import Employee, Department, Role
from datetime import datetime


def index(request):
    return render(request, "index.html")


def all_emp(request):
    emps = Employee.objects.all()
    context = {
        "emps": emps
    }
    return render(request, "view_all_emp.html", context)


def add_emp(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        salary = int(request.POST['salary'])
        bonus = int(request.POST['bonus'])
        phone = int(request.POST['phone'])
        dept_id = int(request.POST['dept'])
        role_id = int(request.POST['role'])
        hire_date = datetime.now()

        department = Department.objects.get(id=dept_id)
        role = Role.objects.get(id=role_id)

        new_emp = Employee(
            first_name=first_name,
            last_name=last_name,
            salary=salary,
            bonus=bonus,
            phone=phone,
            dept=department,
            role=role,
            hire_date=hire_date
        )
        new_emp.save()

        return HttpResponse("Employee added successfully.")
    else:
        departments = Department.objects.all()
        roles = Role.objects.all()
        context = {
            "departments": departments,
            "roles": roles
        }
        return render(request, "add_emp.html", context)


def remove_emp(request, emp_id=0):
    if emp_id:
        try:
            emp_to_be_removed = Employee.objects.get(id=emp_id)
            emp_to_be_removed.delete()
            return HttpResponse("Employee removed successfully")
        except Employee.DoesNotExist:
            return HttpResponse("Invalid employee ID")

    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    return render(request, 'remove_emp.html', context)


def filter_emp(request):
    if request.method == "POST":
        name = request.POST.get("name")
        dept = request.POST.get("dept")
        role = request.POST.get("role")
        emps = Employee.objects.all()

        if name:
            emps = emps.filter(Q(first_name__icontains = name) | Q(last_name__icontains = name))
        if dept:
            emps = emps.filter(dept__name__icontains = dept)
        if role:
            emps = emps.filter(role__name__icontains=role)

        context = {
            "emps": emps
        }
        return render(request, "view_All_emp.html", context)
    elif request.method == "GET":
        return render(request, "filter_emp.html")
    else:
        return HttpResponse("An exception occurred")

