
from django.urls import path, include
from . import views 
from .views import (register, reset_password, dashboard, add_book, book_category, borrow_book, book_instance, borrowed_books
)

urlpatterns = [
    path('', views.home, name="home"),    
    path('register/', views.register, name="register"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('reset-password/', views.reset_password, name="resetpassword"),    
    path('logout/', views.logout, name="logout"),    
    path('add-book/', views.add_book, name="add-book"),    
    path('borrow-book/', views.borrow_book, name="borrow-book"),  
    path('borrowed-books/', views.borrowed_books, name="borrowed-books"),  
    path('notifications/', views.notifications, name="logout"),    
    path('book-category/', views.book_category, name="book-category"), 
    path('view-book/', views.view_book, name="view_book"), 
    path('book-instance/', views.book_instance, name="book-instance"),    
]
