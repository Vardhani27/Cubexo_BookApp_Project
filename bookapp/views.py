import random
from datetime import timedelta
from django.http import Http404
from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout as django_logout, login
from django.contrib import messages
from BookSite import settings
from bookapp.form import BookForm
from bookapp.models import AppUserRole, Book, OTPforRegistration, UsersBooks
from django.core.mail import send_mail


# Create your views here.
def generate_otp(user):
    otp = str(random.randint(1000, 9999))
    expiry = timezone.now() + timedelta(minutes=10)

    OTPforRegistration.objects.create(user=user, otp=otp, otp_expiry=expiry)
    print(f"Generated OTP for {user.username}: {otp}") 
    send_otp_email(user.email,otp)

def send_otp_email(user_email,otp):    
    subject = "Your OTP Code"
    message = f"Hello! Your OTP is: {otp}"
    from_email = "noreply@example.com"
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list)

def ValidateOtp(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        otp_input = request.POST['otp']

        if not user_id:
            messages.error("Session user doesnt exists. Please register first")
            return redirect('register')
        
        try:
            otp_record = OTPforRegistration.objects.get(user_id=user_id, otp=otp_input)
            if otp_record.otp_expiry < timezone.now():
                messages.info(request, 'OTP expired.')
                return redirect('otp')

            otp_record.delete()
            messages.success(request, 'OTP verified successfully. Please login.')
            return redirect('login')  # URL name

        except OTPforRegistration.DoesNotExist:
            messages.error(request, 'Invalid OTP. Please try again.')
            return redirect('otp')
    
    return render(request, 'login related/otp.html')


def Registers(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        role = request.POST.get('role')
        username = request.POST.get('username')

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            messages.info(request, 'User already exists.')
            return render(request, 'login related/register.html')

        # Create Django user
        django_user = User.objects.create_user(
            email=email,
            password=password,
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        AppUserRole.objects.create(user=django_user, role=role)
        generate_otp(django_user)

        request.session['user_id'] = django_user.id

        return redirect('otp')  # make sure URL name matches
    return render(request, 'login related/register.html')



def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            # now get the AppUserRole for role
            app_user = AppUserRole.objects.get(user=user)
            request.session['user_id'] = app_user.id
            request.session['role'] = app_user.role

            if app_user.role:
                return redirect('explore')
            
        else:
            messages.error(request, 'Invalid credentials.')

    return render(request, 'login related/login.html') 


def home(request):
   return render(request, 'home.html')

#reader actions
@login_required(login_url='/login')
def saved_books(request):
    user = request.user
    user_profile = AppUserRole.objects.get(user=user)

    if user_profile.role.lower() != 'reader':
        messages.error(request, 'Access denied. Log in as reader.')
        return redirect('explore')

    user_books = UsersBooks.objects.filter(user=user).select_related('book')
    books = [entry.book for entry in user_books]
    
    return render(request, 'reader/saved_books.html', {'books': books, 'role': user_profile.role})

@login_required(login_url='/login')
def add_to_saved_books(request, book_id):
    user = request.user

    # Get user's role safely
    try:
        role = user.appuserrole.role.lower()
    except:
        messages.error(request, 'User role not found. Please log in again.')
        return redirect('home')

    if role != 'reader':
        messages.error(request, 'Only readers can save books.')
        return redirect('home')

    # Get the book or show 404
    book = get_object_or_404(Book, id=book_id)

    # Save the book
    if UsersBooks.objects.filter(user=user, book=book).exists():
        messages.info(request, f'"{book.title}" is already in your saved books.')
    else:
        UsersBooks.objects.create(user=user, book=book)
        messages.success(request, f'"{book.title}" added to your saved books!')

    return redirect('savedBooks')


def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'book_detail.html', {'book': book, "role": "reader"})


#author actions
@login_required(login_url='/login')
def my_books(request):
    user = request.user
    user_profile = AppUserRole.objects.get(user=user)

    if user_profile.role.lower() != 'author':
        messages.error(request, 'Access denied. Log in as author.')
        return redirect('explore')

    books = Book.objects.filter(author=user)
    return render(request, 'author/my_books.html', {'books': books, "role": user_profile.role})

@login_required(login_url='/login')
def add_book(request):
    if request.session.get('role') != 'author':
        return messages.error("You are not authorized to add books.")

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.author_id = request.session['user_id']
            book.save()
            return redirect('myBooks')
    else:
        form = BookForm()

    return render(request, 'add_book.html', {'form': form})

@login_required(login_url='/login')
def edit_book(request, book_id):
    book = Book.objects.get(id=book_id)
    if request.session.get('user_id') != book.author_id:
        return messages.error("You cannot edit this book.")

    form = BookForm(request.POST or None, request.FILES or None, instance=book)
    if form.is_valid():
        form.save()
        return redirect('myBooks')
    return render(request, 'edit_book.html', {'form': form})

@login_required(login_url='/login')
def delete_book(request, book_id):
    book = Book.objects.get(id=book_id)
    if request.session.get('user_id') != book.author_id:
        return messages.error("You cannot delete this book.")
    book.delete()
    return redirect('myBooks')

def explore(request):
    """
    Shows all books.  If the visitor is a logged-in reader we also display
    an 'Add to My Books' button for each item.
    """

    books = Book.objects.all()
    role = None
    if request.user.is_authenticated:
        try:
            role = request.user.appuserrole.role.lower()
        except AppUserRole.DoesNotExist:
            role = None

    context = {
        'books': books,
        'role': role,
    }
    return render(request, 'explore.html', context)


def logout(request):
    django_logout(request)
    return redirect('explore')

@login_required(login_url='/login')
def profile(request):
    return render(request, 'profile.html')
