import random
from datetime import timedelta
from django.http import Http404, HttpResponseForbidden
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from bookapp.form import BookForm
from bookapp.models import AppUser, Book, OTPforRegistration


# Create your views here.
def generate_otp(user):
    otp = str(random.randint(1000, 9999))
    expiry = timezone.now() + timedelta(minutes=10)

    OTPforRegistration.objects.create(user=user, otp=otp, otp_expiry=expiry)
    print(f"Generated OTP for {user.username}: {otp}") 


def ValidateOtp(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        otp_input = request.POST['otp']
        
        try:
            otp_record = OTPforRegistration.objects.get(user_id=user_id, otp=otp_input)
            if otp_record.otp_expiry < timezone.now():
                messages.info(request, 'OTP expired.')
                return redirect('register/validate-otp')

            otp_record.delete()
            messages.success(request, 'OTP verified successfully. Please login.')
            return redirect('login')  # URL name

        except OTPforRegistration.DoesNotExist:
            messages.error(request, 'Invalid OTP. Please try again.')
            return redirect('register/validate-otp')
    
    return render(request, 'otp.html')


def Registers(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        name = request.POST['name']
        role = request.POST['role']
        username = request.POST['username']

        if AppUser.objects.filter(username=username).exists() or AppUser.objects.filter(email=email).exists():
            messages.info(request, 'User already exists.')
            return render(request, 'register.html')

        user = AppUser.objects.create(
            email=email,
            password=password,
            name=name,
            username=username,
            role=role
        )
        user.save()
        generate_otp(user)
        request.session['user_id'] = user.userId
        return redirect('register/validate-otp')  # URL name
    return render(request, 'register.html')
    

def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = AppUser.objects.get(username=username)
            if user.password == password:  
                request.session['user_id'] = user.userId
                request.session['role'] = user.role
                messages.success(request, f"Welcome, {user.name}")

                if user.role == 'Author':
                    return redirect('author/dashboard')
                else:
                    return redirect('reader/dashboard')  
            
            else:
                messages.error(request, 'Incorrect password.')
        except AppUser.DoesNotExist:
            messages.error(request, 'User not found.')
    
    return render(request, 'login.html')



def home(request):
   return render(request, 'home.html')

@login_required
def author_dashboard(request):
    user_id = request.session.get('user_id')
    books = Book.objects.filter(author_id=user_id)
    return render(request, 'author-home.html', {'books': books})

@login_required
def reader_dashboard(request):
    books = Book.objects.all()
    return render(request, 'reader-home.html', {'books': books})

#reader actions
def add_to_my_books(request, book_id):
    user = request.user

    # Ensure the user is a reader
    if user.role != 'Reader':
        messages.error(request, 'Only readers can save books.')
        return redirect('home')

    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        raise Http404("Book not found")
    user.saved_books.add(book)
    messages.success(request, f'"{book.title}" added to your books!')
    return redirect('book_detail', book_id=book.id)
    
@login_required
def my_books(request):
    user = request.user
    if user.role != 'Reader':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    books = user.saved_books.all()
    return render(request, 'my_books.html', {'books': books})


#author actions
@login_required
def add_book(request):
    if request.session.get('role') != 'Author':
        return HttpResponseForbidden("You are not authorized to add books.")

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.author_id = request.session['user_id']
            book.save()
            return redirect('author/dashboard')
    else:
        form = BookForm()

    return render(request, 'add_book.html', {'form': form})

@login_required
def edit_book(request, book_id):
    book = Book.objects.get(id=book_id)
    if request.session.get('user_id') != book.author_id:
        return HttpResponseForbidden("You cannot edit this book.")

    form = BookForm(request.POST or None, request.FILES or None, instance=book)
    if form.is_valid():
        form.save()
        return redirect('author/dashboard')
    return render(request, 'edit_book.html', {'form': form})

@login_required
def delete_book(request, book_id):
    book = Book.objects.get(id=book_id)
    if request.session.get('user_id') != book.author_id:
        return HttpResponseForbidden("You cannot delete this book.")
    book.delete()
    return redirect('author/dashboard')


# def logout(request):
#     auth.logout(request)
#     return redirect('home')

