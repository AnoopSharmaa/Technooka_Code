from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import UserManager
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator
)


class User(AbstractUser):

    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30,null=True, blank=True)

    ROLE_CHOICES = (
        ('STUDENT', 'STUDENT'),
        ('LIBRARIAN', 'LIBRARIAN'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']
    objects = UserManager()
    def __str__(self):
        return self.email
    
    class Meta:
        db_table = 'User'


class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'Author'

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'Genre'


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE,related_name='books')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE,related_name='books')
    isbn = models.CharField(max_length=20, unique=True)
    available_copies = models.IntegerField()
    total_copies = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'Book'


class BorrowRequest(models.Model):

    class Status(models.TextChoices):

        PENDING = 'PENDING', 'Pending'
        APPROVED = 'APPROVED', 'Approved'
        REJECTED = 'REJECTED', 'Rejected'
        RETURNED = 'RETURNED', 'Returned'
   
    book = models.ForeignKey(Book, on_delete=models.CASCADE,related_name='borrow_requests')
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='borrow_requests')
    requested_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    return_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    def __str__(self):
        return f"{self.user.email} - {self.book.title} - {self.status}"
    
    class Meta:
        db_table = 'BorrowRequest'


class BookReview(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE,related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='reviews')
    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.book.title} - {self.rating}"
    
    class Meta:
        db_table = 'BookReview'