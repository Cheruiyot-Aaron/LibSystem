from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import User, Book, Borrow, Reservation, Fine, Log, Category, Author, BookInstance, Notification, Report

# Customizing the User admin to manage user types
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type', 'is_active', 'is_staff')
    list_filter = ('user_type', 'is_active', 'is_staff')
    search_fields = ('username', 'email')

admin.site.register(User, UserAdmin)


# Admin configuration for the Book model
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'total_copies', 'available_copies', 'category')
    search_fields = ('title', 'author', 'isbn')
    list_filter = ('category',)

admin.site.register(Book, BookAdmin)


# Admin configuration for the Borrow model
class BorrowAdmin(admin.ModelAdmin):
    list_display = ('student', 'book', 'borrow_date', 'due_date', 'returned')
    list_filter = ('returned', 'borrow_date')
    search_fields = ('student__username', 'book__title')

admin.site.register(Borrow, BorrowAdmin)


# Admin configuration for the Reservation model
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('student', 'book', 'reservation_date', 'fulfilled')
    list_filter = ('fulfilled',)
    search_fields = ('student__username', 'book__title')

admin.site.register(Reservation, ReservationAdmin)


# Admin configuration for the Fine model
class FineAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount', 'reason', 'paid')
    list_filter = ('paid',)
    search_fields = ('student__username',)

admin.site.register(Fine, FineAdmin)


# Admin configuration for the Log model
class LogAdmin(admin.ModelAdmin):
    list_display = ('action', 'user', 'timestamp')
    list_filter = ('action', 'timestamp')
    search_fields = ('user__username', 'description')

admin.site.register(Log, LogAdmin)


# Admin configuration for the Category model
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

admin.site.register(Category, CategoryAdmin)


# Admin configuration for the Author model
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'biography')
    search_fields = ('first_name', 'last_name')

admin.site.register(Author, AuthorAdmin)


# Admin configuration for the BookInstance model
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'copy_number', 'status', 'borrower')
    list_filter = ('status',)
    search_fields = ('book__title', 'copy_number')

admin.site.register(BookInstance, BookInstanceAdmin)


# Admin configuration for the Notification model
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_at', 'read')
    list_filter = ('read',)
    search_fields = ('user__username', 'message')

admin.site.register(Notification, NotificationAdmin)


# Admin configuration for the Report model
class ReportAdmin(admin.ModelAdmin):
    list_display = ('generated_by', 'generated_at')
    search_fields = ('generated_by__username', 'report_data')

admin.site.register(Report, ReportAdmin)
