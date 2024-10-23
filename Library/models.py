from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPES = [
        ('student', 'Student'),
        ('librarian', 'Librarian'),
        ('admin', 'Admin'),
    ]
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='student')

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='library_user_set',  # Custom related_name to avoid conflict
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='library_user_permissions_set',  # Custom related_name to avoid conflict
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)  # Unique identifier for books
    publisher = models.CharField(max_length=255)
    publication_date = models.DateField()
    total_copies = models.IntegerField()
    available_copies = models.IntegerField()

    def __str__(self):
        return self.title
    
    # Category field now references the Category model
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.title} by {self.author}"


class Borrow(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'student'})
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    returned = models.BooleanField(default=False)
    return_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.student} borrowed {self.book}"  


class Reservation(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'student'})
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reservation_date = models.DateTimeField(auto_now_add=True)
    fulfilled = models.BooleanField(default=False)  # Becomes True when the book becomes available and is borrowed

    def __str__(self):
        return f"{self.student} reserved {self.book}"


class Fine(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'student'})
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    reason = models.TextField()  # Reason for the fine, e.g., late return, damaged book
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Fine for {self.student} - {self.amount}"


class Log(models.Model):
    ACTION_CHOICES = [
        ('borrow', 'Borrow'),
        ('return', 'Return'),
        ('fine', 'Fine Issued'),
        ('role_change', 'Role Change'),
        ('book_add', 'Book Added'),
        ('book_update', 'Book Updated'),
        ('book_remove', 'Book Removed'),
    ]
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User who performed the action
    description = models.TextField()  # Optional description for more detail
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} by {self.user} on {self.timestamp}"


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    biography = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class BookInstance(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    copy_number = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=20, default='available')  # Available, Borrowed, Reserved
    borrower = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='borrower')

    def __str__(self):
        return f"{self.book.title} - Copy {self.copy_number}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username} - {self.message[:50]}"


class Report(models.Model):
    generated_by = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'admin'})
    generated_at = models.DateTimeField(auto_now_add=True)
    report_data = models.TextField()  # Store as JSON, or create complex reporting systems with other fields

    def __str__(self):
        return f"Report generated by {self.generated_by} on {self.generated_at}"
