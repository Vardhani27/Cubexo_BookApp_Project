<<<<<<< HEAD

from django.utils import timezone
from django.db import models

class AppUser(models.Model):
    ROLE_CHOICES = (
        ('author', 'Author'),
        ('reader', 'Reader'),
    )
    
    userId = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=200, unique=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.role})"


class OTPforRegistration(models.Model):
    user = models.OneToOneField(AppUser, on_delete=models.CASCADE)
    otp = models.IntegerField(default=0000)
    otp_expiry = models.DateTimeField(default = timezone.now())
    max_otp_try = models.IntegerField(default=3)

    def __str__(self):
        return f"OTP for {self.user.username}"


class Book(models.Model):
    title = models.CharField(max_length=80)
    description = models.TextField(max_length=2000)
    pages = models.PositiveIntegerField()
    category = models.CharField(max_length=80)
    author = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='books')

    cover = models.ImageField(upload_to='book-cover/', blank=True, null=True)
    pdf_file = models.FileField(upload_to='book-pdf/', blank=True, null=True)

    def __str__(self):
        return self.title

    def short_description(self):
        words = self.description.split()
        return ' '.join(words[:50]) + '...' if len(words) > 50 else self.description


#mapping class
class UsersBooks(models.Model):
    userbook = models.AutoField(primary_key=True)
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='saved_books')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='saved_by_users')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"
=======
from django.db import models

# Create your models here.
   

class User(models.Model):

    ROLE_CHOICES = (
        ('author', 'Author'),
        ('reader', 'Redader')
    )
    userId = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=200, null=False, unique = True)
    name = models.CharField(max_length=200, null=True, blank=True)
    password = models.CharField(max_length=10, null=False)
    username = models.CharField(max_length=100, null=False, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, null= False, blank= False)


    class Meta:
        app_label = 'bookapp' 


    def __str__(self):
        return self.name

    def edit(self, image, phone):
        self.image = image
        self.phone = phone
        self.save()


class OTPforRegistration(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE )
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_expiry = models.DateTimeField(blank=True, null=True)

    class Meta:
        app_label = 'bookapp' 


class Books(models.Model):
    title = models.CharField(max_length = 80)
    summary = models.TextField(max_length=2000)
    pages = models.CharField(max_length=80)
    author = models.CharField(max_length=80)
    category = models.CharField(max_length=80)
    author_id = models.ForeignKey(User, max_length=200, on_delete=models.CASCADE)

    class Meta:
        app_label = 'bookapp' 

    def __str__(self):
        return f"{self.title}"

    def short_description(self):
        words = self.summary.split()
        if len(words) > 50:
            return ' '.join(words[:30]) + '...'
        else:
            return self.summary
>>>>>>> 91cc36d3eb3bd182817efc3ff53ca5e604607ad6
