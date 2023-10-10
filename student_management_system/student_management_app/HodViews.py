from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

from student_management_app.models import Courses, CustomUser, Staffs, Students, Subjects


def admin_home(request):
    return render(request, "hod_template/home_content.html")

def add_staff(request):
    return render(request, "hod_template/add_staff_template.html")

def add_staff_save(request):
    if request.method!="POST":
        return HttpResponse("Method not Allowed")
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        address=request.POST.get("address")
        try:
            user=CustomUser.objects.create_user(username=username, password=password, email=email , first_name=first_name, last_name=last_name, user_type=2)
            user.staffs.address=address
            user.save()
            messages.success(request, "Staff Added Successfully")
            return HttpResponseRedirect("/add_staff")
            
        except:
            messages.error(request, "Failed to Add Staff")
            return HttpResponseRedirect("/add_staff") 
        

def add_course(request):
    return render(request, "hod_template/add_course_template.html")
        

def add_course_save(request):
    if request.method!="POST":
        return HttpResponse("Method not Allowed")
    else:
        course=request.POST.get("course")
        try:
            course_model=Courses(course_name=course)
            course_model.save()
            messages.success(request, "Course Added Successfully")
            return HttpResponseRedirect("/add_course")
        except:
            messages.error(request, "Failed to Add Course")
            return HttpResponseRedirect("/add_course") 

def add_subject(request):
    courses=Courses.objects.all()
    staffs=CustomUser.objects.filter(user_type=2)
    return render(request, "hod_template/add_subject_template.html", {"courses":courses, "staffs":staffs})

def add_subject_save(request):
    if request.method!="POST":
        return HttpResponse("Method not Allowed")
    
    else:
        subject_name=request.POST.get("subject_name")
        course_id=request.POST.get("course")
        course=Courses.objects.get(id=course_id)
        staff_id=request.POST.get("staff")
        staff=CustomUser.objects.get(id=staff_id)
        
        try:
            subject=Subjects(subject_name=subject_name, course_id=course, staff_id=staff)
            subject.save()
            messages.success(request, "Subject Added Successfully")
            return HttpResponseRedirect("/add_subject")
            
        except:
            messages.error(request, "Failed to Add Subject")
            return HttpResponseRedirect("/add_subject") 
    
        

def add_student(request):
    courses=Courses.objects.all()
    return render(request, "hod_template/add_student_template.html", {"courses":courses})

def add_student_save(request):
    if request.method!="POST":
        return HttpResponse("Method not Allowed")
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        address=request.POST.get("address")
        session_start=request.POST.get("session_start")
        session_end=request.POST.get("session_end")
        course_id=request.POST.get("course")
        gender=request.POST.get("gender")
        
        profile_pic=request.FILES['profile_pic']
        fs=FileSystemStorage()
        filename=fs.save(profile_pic.name, profile_pic)
        profile_pic_url=fs.url(filename)
        
        try:
            user=CustomUser.objects.create_user(username=username, password=password, email=email , first_name=first_name, last_name=last_name, user_type=3)
            user.students.address=address
            course_obj=Courses.objects.get(id=course_id)
            user.students.course_id=course_obj
            user.students.session_start_year=session_start
            user.students.session_end_year=session_end
            user.students.gender=gender
            user.students.profile_pic=profile_pic_url
            user.save()
            messages.success(request, "Student Added Successfully")
            return HttpResponseRedirect("/add_staff")
            
        except:
            messages.error(request, "Failed to Add Student")
            return HttpResponseRedirect("/add_student") 
        

def manage_staff(request):
    staffs=Staffs.objects.all()
    return render(request, "hod_template/manage_staff.html", {"staffs":staffs})

def manage_student(request):
    students=Students.objects.all()
    return render(request, "hod_template/manage_student.html", {"students":students})


def manage_course(request):
    courses=Courses.objects.all()
    return render(request, "hod_template/manage_course.html", {"courses":courses})


def manage_subject(request):
    subjects=Subjects.objects.all()
    return render(request, "hod_template/manage_subject.html", {"subjects":subjects})


def edit_staff(request, staff_id):
    staff=Staffs.objects.get(admin=staff_id)
    return render(request, "hod_template/edit_staff_template.html", {"staff":staff, "id":staff_id})


def edit_staff_save(request):
    if request.method!="POST":
        return HttpResponse("Method not Allowed")
    else:
        staff_id=request.POST.get("staff_id")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        email=request.POST.get("email")
        username=request.POST.get("username")
        address=request.POST.get("address")
        
        try:
            user=CustomUser.objects.get(id=staff_id)
            
            user.first_name=first_name
            user.last_name=last_name
            user.email=email
            user.username=username
            user.save()
            
            staff_model=Staffs.objects.get(admin=staff_id)
            staff_model.address=address
            staff_model.save()

            messages.success(request, "Staff Edited Successfully")
            return HttpResponseRedirect("/edit_staff/"+staff_id)
        
        except:
            messages.error(request, "Failed to Edit Staff")
            return HttpResponseRedirect("/edit_staff/"+staff_id) 
        
        
def edit_student(request, student_id):
    courses=Courses.objects.all()
    student=Students.objects.get(admin=student_id)
    return render(request, "hod_template/edit_student_template.html", {"student":student, "courses":courses, "id":student_id})


def edit_student_save(request):
    if request.method!="POST":
        return HttpResponse("Method not Allowed")
    
    else:
        student_id=request.POST.get("student_id")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
        email=request.POST.get("email")
        address=request.POST.get("address")
        session_start=request.POST.get("session_start")
        session_end=request.POST.get("session_end")
        course_id=request.POST.get("course")
        gender=request.POST.get("gender")
        
        if request.FILES.get('profile_pic', False):
            profile_pic=request.FILES['profile_pic']
            fs=FileSystemStorage()
            filename=fs.save(profile_pic.name, profile_pic)
            profile_pic_url=fs.url(filename)
        else:
            profile_pic_url=None
        
        try:
            user=CustomUser.objects.get(id=student_id)
            user.first_name=first_name
            user.last_name=last_name
            user.username=username
            user.email=email
            user.save()
            
            student=Students.objects.get(admin=student_id)
            student.address=address
            student.session_start_year=session_start
            student.session_end_year=session_end
            student.gender=gender
            course=Courses.objects.get(id=course_id)
            student.course_id=course
            if profile_pic_url!=None:
                student.profile_pic=profile_pic_url
            student.save()  
            
            messages.success(request, "Student Edited Successfully")
            return HttpResponseRedirect("/edit_student/"+student_id)
        
        except:
            messages.error(request, "Failed to Edit Student")
            return HttpResponseRedirect("/edit_student/"+student_id) 




def edit_subject(request, subject_id):
    subject=Subjects.objects.get(id=subject_id)
    courses=Courses.objects.all()
    staffs=CustomUser.objects.filter(user_type=2)
    
    return render(request, "hod_template/edit_subject_template.html", {"subject":subject, "courses":courses, "staffs":staffs, "id":subject_id})


def edit_subject_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        subject_id=request.POST.get("subject_id")
        subject_name=request.POST.get("subject_name")
        staff_id=request.POST.get("staff")
        course_id=request.POST.get("course")
        
        try:
            subject=Subjects.objects.get(id=subject_id)
            subject.subject_name=subject_name
            staff=CustomUser.objects.get(id=staff_id)
            subject.staff_id=staff
            course=Courses.objects.get(id=course_id)
            subject.course_id=course
            subject.save()
            
            messages.success(request, "Subject Edited Successfully")
            return HttpResponseRedirect("/edit_subject_save/"+subject_id)
        
        except:
            messages.error(request, "Failed to Edit Subject")
            return HttpResponseRedirect("/edit_subject_save/"+subject_id) 


def edit_course(request, course_id):
    course=Courses.objects.get(id=course_id)
    return render(request, "hod_template/edit_course_template.html", {"course":course, "id":course_id})


def edit_course_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        course_id=request.POST.get("course_id")
        course_name=request.POST.get("course")
        
        try:
            course=Courses.objects.get(id=course_id)
            course.course_name=course_name
            course.save()
            
            messages.success(request, "Course Edited Successfully")
            return HttpResponseRedirect("/edit_course/"+course_id)
        
        except:
            messages.error(request, "Failed to Edit Course")
            return HttpResponseRedirect("/edit_course/"+course_id) 