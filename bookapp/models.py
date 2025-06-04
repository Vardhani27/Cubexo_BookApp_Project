
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

class AppUserRole(models.Model):
    ROLE_CHOICES = (
        ('author', 'Author'),
        ('reader', 'Reader'),
    )
    
    id = models.AutoField(primary_key=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    user = models.OneToOneField(User, on_delete=models.CASCADE) #has email, password and username

    def __str__(self):
        return f"{self.role}"


class OTPforRegistration(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')

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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_books')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='saved_by_users')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"
