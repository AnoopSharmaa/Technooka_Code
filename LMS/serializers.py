from time import timezone

from rest_framework import serializers
from .models import User,Author, Genre, Book, BookReview, BorrowRequest


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'password',
            'role'
        ]
        extra_kwargs = {
            'email': {
                'validators': []
            }
        }

    # First Name Validation
    def validate_first_name(self, value):

        if len(value.strip()) < 3:
            raise serializers.ValidationError(
                "First name must contain at least 3 characters."
            )

        return value

    # Email Validation
    def validate_email(self, value):

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Email already exists."
            )

        return value

    def create(self, validated_data):

        password = validated_data.pop('password')

        user = User(**validated_data)

        user.set_password(password)

        user.save()

        return user
    

from rest_framework import serializers
from .models import Book


class BookListSerializer(serializers.ModelSerializer):

    author = serializers.StringRelatedField()
    genre = serializers.StringRelatedField()

    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'author',
            'genre',
            'isbn',
            'available_copies',
            'total_copies'
        ]




from rest_framework import serializers

from .models import (
    Book,
    Author,
    Genre,
    BookReview
)


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author

        fields = [
            'id',
            'name',
            'bio'
        ]


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre

        fields = [
            'id',
            'name'
        ]


class BookReviewSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField()

    class Meta:
        model = BookReview

        fields = [
            'user',
            'rating',
            'comment',
            'created_at'
        ]


class BookDetailSerializer(serializers.ModelSerializer):

    author = AuthorSerializer(
        read_only=True
    )

    genre = GenreSerializer(
        read_only=True
    )

    reviews = BookReviewSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Book

        fields = [
            'id',
            'title',
            'author',
            'genre',
            'isbn',
            'available_copies',
            'total_copies',
            'reviews'
        ]



class BookCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book

        fields = [
            'title',
            'author',
            'genre',
            'isbn',
            'available_copies',
            'total_copies'
        ]

    def validate(self, data):

        if data['available_copies'] > data['total_copies']:
            raise serializers.ValidationError(
                "Available copies cannot exceed total copies."
            )

        return data
    

class BorrowRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = BorrowRequest

        fields = [
            'id',
            'book'
        ]

    def validate(self, data):

        request = self.context['request']

        book = data['book']

        # Check book availability
        if book.available_copies <= 0:

            raise serializers.ValidationError(
                {
                    "book": [
                        "Book is not available."
                    ]
                }
            )

        # Check existing borrow request
        existing_request = BorrowRequest.objects.filter(
            user=request.user,
            book=book,
            status__in=[
                BorrowRequest.Status.PENDING,
                BorrowRequest.Status.APPROVED
            ]
        ).exists()

        if existing_request:

            raise serializers.ValidationError(
                {
                    "book": [
                        "You already have an active request for this book."
                    ]
                }
            )

        return data

class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book

        fields = [
            'id',
            'title',
            'author',
            'genre',
            'isbn',
            'available_copies',
            'total_copies'
        ]   

class BorrowRequestListSerializer(serializers.ModelSerializer):

    book = BookSerializer(
        read_only=True  )

    class Meta:
        model = BorrowRequest

        fields = [
            'id',
            'book',
            'status',
            'requested_at',
            'approved_at',
            'return_at'
        ]




class BookReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookReview

        fields = [
            'id',
            'book',
            'rating',
            'comment'
        ]

    def validate_rating(self, value):

        if value < 1 or value > 5:
            raise serializers.ValidationError(
                "Rating must be between 1 and 5"
            )

        return value



