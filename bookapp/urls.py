from django.urls import path
from bookapp import views

urlpatterns = [
  path('home', views.home, name='home'),
  # path('explore', views.explore, name='explore'),
  path('register', views.Registers, name='register'),
  path('register/validate-otp', views.ValidateOtp, name='otp'),
  path('login', views.Login, name='login'),
  # path('addBook/<int:user_id>', views.addBook, name='addBook'),
  # path('addBook', views.addBook, name='addBook'),
  # path('logout', views.logout, name='logout'),
  # path('deleteBook/<int:book_id>', views.deleteBook, name='deleteBook'),
  # path('editBook/<int:book_id>', views.editBook, name='editBook'),
  # path('viewBook/<int:book_id>', views.viewBook, name='viewBook'),
]