from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout 
from .models import Category, Book

# Create your views here.
def home(request):
    if request.method == 'POST':
        # Fetching the username from the POST request instead of email
        username = request.POST['username']  # Changed from 'email' to 'username'
        password = request.POST['password']

        # Authenticate using username and password
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # If authentication is successful, log the user in
            login(request, user)
            return redirect('dashboard')  # Adjust 'dashboard/' to the correct path
        else:
            # If login fails, send error message
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        email = request.POST['email']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Basic validation
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        # if User.objects.filter(email=email).exists():
        #     messages.error(request, "Email already registered.")
        #     return redirect('register')

        # Create new user
        user = User.objects.create_user(username=username, password=password1, email=email)
        user.first_name = full_name
        user.save()
        
         # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, f"Username '{username}' already exists. Please try another.")
            return render(request, 'register.html', {
                'full_name': full_name, 'email': email, 'username': ''
            })

        # Check if email already exists
        # if User.objects.filter(email=email).exists():
        #     messages.error(request, f"An account with email '{email}' already exists. Please use another email.")
        #     return render(request, 'register.html', {
        #         'full_name': full_name, 'email': '', 'username': username
        #     })

        # If all checks pass, create the new user
        user = User.objects.create_user(username=username, password=password1, email=email)
        user.first_name = full_name
        user.save()

        messages.success(request, "Account created successfully.")
        return redirect('/')  # redirect to the login page after successful registration
    return render(request, 'register.html')

def reset_password(request):
    return render(request, 'reset_password.html')

def dashboard(request):
     return render(request, 'dashboard.html')
 
def add_book(request):
    return render(request, 'add-book.html')

def book_instance(request):
    return render(request, 'book_instance.html')

def borrow_book(request):
    return render(request, 'borrow-book.html')

def notifications(request):
    return render(request, 'notifications.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def view_book(request):
    return render(request, 'view-book.html') 

def book_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')  # Fetch the category name from form input

        if category_name:  # Ensure the input field is not empty
            # Check if the category already exists
            if not Category.objects.filter(name=category_name).exists():
                # Create and save a new category if it doesn't exist
                Category.objects.create(name=category_name)
                messages.success(request, f"Category '{category_name}' added successfully!")
            else:
                # Notify the user that the category already exists
                messages.error(request, f"Category '{category_name}' already exists.")
        else:
            # Notify the user that the category name cannot be empty
            messages.error(request, 'Category name cannot be empty.')

        # Redirect to the same page after handling the POST request
        return redirect('book-category')

    # Fetch all categories to display them in the template
    categories = Category.objects.all()

    context = {
        'categories': categories,  # Pass the list of categories to the template
    }

    # Render the template with the context
    return render(request, 'book-category.html', context) 

def add_book(request):
    if request.method == 'POST':
        # Capture data from the form
        title = request.POST.get('title')
        author = request.POST.get('author')
        isbn = request.POST.get('isbn')
        publisher = request.POST.get('publisher')
        publication_date = request.POST.get('publication_date')
        total_copies = request.POST.get('total_copies')
        available_copies = request.POST.get('available_copies')
        category_id = request.POST.get('category')  # Selected category ID from dropdown

        # Fetch the selected category object from the database
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            category = None
        
        # Validation: Ensure required fields are not empty
        if not (title and author and isbn and publisher and publication_date and total_copies and available_copies and category):
            messages.error(request, 'All fields are required.')
            return redirect('add-book')  # Replace with your URL name for this page

        # Check if a book with the same ISBN already exists
        if Book.objects.filter(isbn=isbn).exists():
            messages.error(request, f"A book with ISBN '{isbn}' already exists.")
        else:
            # Create and save the new book entry
            Book.objects.create(
                title=title,
                author=author,
                isbn=isbn,
                publisher=publisher,
                publication_date=publication_date,
                available_copies=available_copies,
                category=category
            )
            messages.success(request, f"Book '{title}' added successfully!")

        # Redirect to the same page after the form submission
        return redirect('add-book')

    # If it's a GET request, fetch categories to display in the form dropdown
    categories = Category.objects.all()

    context = {
        'categories': categories,  # Pass categories to the template for the dropdown
    }

    return render(request, 'add-book.html', context)
