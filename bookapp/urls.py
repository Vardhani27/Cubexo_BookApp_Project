from django.urls import path
from bookapp import views

urlpatterns = [
  
  path('register', views.Registers, name='register'),
  path('register/validate-otp', views.ValidateOtp, name='otp'),
  path('login', views.Login, name='login'),
  path('logout', views.logout, name='logout'),

  path('saved-books', views.saved_books, name='savedBooks'),
  path('my-books', views.my_books, name='myBooks'),
  path('', views.explore, name='explore'),
  path('user-profile', views.profile , name='profile'),
  
  
  path('addBook/<int:user_id>', views.add_book, name='addBook'),
  path('save/<int:book_id>', views.add_to_saved_books, name='saveBook'),
  path('book/<int:book_id>/', views.book_detail, name='book_detail'),
  path('addBook', views.add_book, name='addBook'),
  path('deleteBook/<int:book_id>', views.delete_book, name='deleteBook'),
  path('editBook/<int:book_id>', views.edit_book, name='editBook'),
  
]