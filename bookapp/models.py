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