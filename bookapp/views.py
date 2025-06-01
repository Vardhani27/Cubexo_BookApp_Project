from datetime import datetime, timezone
import random
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render

# Create your views here.
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from flask import Response


from bookapp.models import OTPforRegistration

# Create your views here.
def home(request):
    return render(request, 'main.html', {})




def generateOTP():
    otp = random.randint(1000, 9999)
    otp_expiry = timezone.now() + datetime.timedelta(minutes=10)
    max_otp_try = int(OTPforRegistration.max_otp_try) - 1

    entry = OTPforRegistration.objects.create(otp = otp, otp_expiry = otp_expiry, max_otp_try = max_otp_try)
    entry.save()



    




def Registers(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        name = request.POST['name']
        phone = request.POST['phone']
        role = request.POST['role']
        Username = request.POST['username']

        if User.objects.filter(Username=Username).exists() or User.objects.filter(email=email).exists():
            messages.info(request,'User already exists')
            return render(request, 'register.html')
            
            
        else:
            register = User.objects.create_user(email=email,password=password,name=name,phone=phone,role=role,username=Username )
            register.save()
            generateOTP()
            return HttpResponseRedirect('register/otp')
            
        
    else:
        return render(request, 'register.html')

    
def ValidateOtp(request):
    if request.method == "POST":
        otp = request.POST["otp"]

        if OTPforRegistration.objects.filter(otp == otp).exists():
            HttpResponseRedirect('login')
            otp.delete()


        else:
            messages.info(request, "re-enter correct OTP.")
    else:
        return render(request, 'otp.html')
    

def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            print('User logged in successfully')
            return redirect('home')
        else:
            messages.info(request,'Invalid Credentials')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


def home(request):
   return render(request, 'home.html')



# def explore(request):
#     edu_books = EBooksModel.objects.filter(category='Education')
#     fiction_books = EBooksModel.objects.filter(category='Fiction')
#     science_books = EBooksModel.objects.filter(category='Science')
#     return render(request, 'explore.html',{'edu_books':edu_books,'fiction_books':fiction_books,'science_books':science_books})

# @login_required
# def addBook(request,user_id):
#     user = User.objects.get(id=user_id)
#     if request.method == 'POST':
#         form = EBooksForm(request.POST, request.FILES)
#         if form.is_valid():
#             book = form.save(commit=False)
#             book.author = user.first_name + " " + user.last_name
#             book.author_id = user.id
#             print(book.author)
#             book.save()
#             print()
#             print()
#             print(book.author)
#             print("Book saved successfully")
#             print()
#             print()
#             return redirect('home')
#         else:
#             print(form.errors)
#     else:
#         form = EBooksForm()
#     return render(request, 'addBook.html', {'form': form})

# def contri(request,user_id):
#     books = EBooksModel.objects.filter(author_id=user_id)
#     return render(request, 'contri.html', {'books': books})


# def logout(request):
#     auth.logout(request)
#     return redirect('home')

# def deleteBook(request,book_id):
#     book = EBooksModel.objects.get(id=book_id)
#     book.delete()
#     return redirect('home')

# def editBook(request,book_id):
#     book = EBooksModel.objects.get(id=book_id)
#     if request.method == 'POST':
#         form = EBooksForm(request.POST, request.FILES,instance=book)
#         if form.is_valid():
#             form.save()
#             print()
#             print()
#             print("Book updated successfully")
#             print()
#             print()
#             return redirect('home')
#         else:
#             print(form.errors)
#     else:
#         form = EBooksForm(instance=book)
#     return render(request, 'editBook.html', {'form': form,'book':book})

# def viewBook(request,book_id):
#     book = EBooksModel.objects.get(id=book_id)
#     book.summary = book.summary.replace('\n', '<br/>')
#     return render(request, 'viewBook.html', {'book': book})
