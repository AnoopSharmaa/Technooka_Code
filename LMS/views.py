from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView, Http404
from rest_framework import status

from LMS.throttles import BorrowRequestThrottle

from .utils.response import (
    success_response,
    error_response
)
from django.shortcuts import get_object_or_404
from .serializers import BookReviewSerializer, BorrowRequestListSerializer, RegisterSerializer,BookDetailSerializer,BookListSerializer, BookCreateSerializer, AuthorSerializer,GenreSerializer,BorrowRequestSerializer,BorrowRequestListSerializer


from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated,AllowAny
from .permission import IsLibrarian, IsStudent, IsOwnerOrReadOnly

from .models import Book,Author, Genre, BookReview,BorrowRequest
from .filters import BookFilter


class RegisterView(APIView):

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return success_response(
                message="User Registered Successfully",
                data=serializer.data,
                status_code=status.HTTP_201_CREATED
            )

        return error_response(
            message="Validation Error",
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )
    


class BookView(APIView):

    def get_permissions(self):

        if self.request.method == 'GET':

            permission_classes = [AllowAny]

        elif self.request.method == 'POST':

            permission_classes = [
                IsAuthenticated,
                IsLibrarian
            ]

        return [
            permission()
            for permission in permission_classes
        ]

    def get(self, request):

        queryset = Book.objects.select_related(
            'author',
            'genre'
        ).all()

        # Apply Filters
        filtered_queryset = BookFilter(
            request.GET,
            queryset=queryset
        ).qs

        serializer = BookListSerializer(
            filtered_queryset,
            many=True
        )

        return success_response(
            message="Books fetched successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )

    # CREATE BOOK
    def post(self, request):

        serializer = BookCreateSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return success_response(
                message="Book added successfully",
                data=serializer.data,
                status_code=status.HTTP_201_CREATED
            )

        return error_response(
            message="Validation Error",
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )
    

class BookDetailView(APIView):

    def get_permissions(self):

        if self.request.method == 'GET':

            permission_classes = [AllowAny]

        else:

            permission_classes = [
                IsAuthenticated,
                IsLibrarian
            ]

       # Debugging line to check permissions

        return [
            permission()
            for permission in permission_classes
        ]

    # COMMON METHOD TO FETCH BOOK
    def get_object(self, pk):

        return get_object_or_404(
            Book.objects.select_related(
                'author',
                'genre'
            ).prefetch_related(
                'reviews__user'
            ),
            pk=pk
        )

    # GET BOOK DETAIL
    def get(self, request, pk):

        try:

            book = self.get_object(pk)

            serializer = BookDetailSerializer(book)

            return success_response(
                message="Book fetched successfully",
                data=serializer.data,
                status_code=status.HTTP_200_OK
            )

        except Http404:

            return error_response(
                message="Book not found",
                errors={
                    "book": [
                        "No Book matches the given query."
                    ]
                },
                status_code=status.HTTP_404_NOT_FOUND
            )

    # FULL UPDATE
    def put(self, request, pk):

        try:

            book = self.get_object(pk)

            serializer = BookCreateSerializer(
                book,
                data=request.data
            )

            if serializer.is_valid():

                serializer.save()

                return success_response(
                    message="Book updated successfully",
                    data=serializer.data,
                    status_code=status.HTTP_200_OK
                )

            return error_response(
                message="Validation Error",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        except Http404:

            return error_response(
                message="Book not found",
                errors={
                    "book": [
                        "No Book matches the given query."
                    ]
                },
                status_code=status.HTTP_404_NOT_FOUND
            )

    # PARTIAL UPDATE
    def patch(self, request, pk):

        try:

            book = self.get_object(pk)

            serializer = BookCreateSerializer(
                book,
                data=request.data,
                partial=True
            )

            if serializer.is_valid():

                serializer.save()

                return success_response(
                    message="Book partially updated successfully",
                    data=serializer.data,
                    status_code=status.HTTP_200_OK
                )

            return error_response(
                message="Validation Error",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        except Http404:

            return error_response(
                message="Book not found",
                errors={
                    "book": [
                        "No Book matches the given query."
                    ]
                },
                status_code=status.HTTP_404_NOT_FOUND
            )

    # DELETE BOOK
    def delete(self, request, pk):

        try:

            book = self.get_object(pk)

            book.delete()

            return success_response(
                message="Book deleted successfully",
                data={},
                status_code=status.HTTP_200_OK
            )

        except Http404:

            return error_response(
                message="Book not found",
                errors={
                    "book": [
                        "No Book matches the given query."
                    ]
                },
                status_code=status.HTTP_404_NOT_FOUND
            )
    




class AuthorView(APIView):

    # DYNAMIC PERMISSIONS
    def get_permissions(self):

        # GET -> Public Access
        if self.request.method == 'GET':

            permission_classes = [AllowAny]

        # POST -> Librarian Only
        else:

            permission_classes = [
                IsAuthenticated,
                IsLibrarian
            ]

        return [
            permission()
            for permission in permission_classes
        ]

    # LIST AUTHORS
    def get(self, request):

        authors = Author.objects.all()

        serializer = AuthorSerializer(
            authors,
            many=True
        )

        return success_response(
            message="Authors fetched successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )

    # CREATE AUTHOR
    def post(self, request):

        serializer = AuthorSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return success_response(
                message="Author created successfully",
                data=serializer.data,
                status_code=status.HTTP_201_CREATED
            )

        return error_response(
            message="Validation Error",
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )
    


class GenreView(APIView):

    # DYNAMIC PERMISSIONS
    def get_permissions(self):

        # GET -> Public Access
        if self.request.method == 'GET':

            permission_classes = [AllowAny]

        # POST -> Librarian Only
        else:

            permission_classes = [
                IsAuthenticated,
                IsLibrarian
            ]

        return [
            permission()
            for permission in permission_classes
        ]

    # LIST GENRES
    def get(self, request):

        genres = Genre.objects.all()

        serializer = GenreSerializer(
            genres,
            many=True
        )

        return success_response(
            message="Genres fetched successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )

    # CREATE GENRE
    def post(self, request):

        serializer = GenreSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return success_response(
                message="Genre created successfully",
                data=serializer.data,
                status_code=status.HTTP_201_CREATED
            )

        return error_response(
            message="Validation Error",
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )
    


class BorrowRequestView(APIView):
    permission_classes = [IsAuthenticated,IsStudent]
    # throttle_classes = [BorrowRequestThrottle]


    def post(self, request):

        serializer = BorrowRequestSerializer(
            data=request.data,context={'request': request}
        )

        if serializer.is_valid():

            serializer.save(
                user=request.user
            )

            return success_response(
                message="Borrow request created successfully",
                data=serializer.data,
                status_code=status.HTTP_201_CREATED
            )

        return error_response(
            message="Validation Error",
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    def get(self, request):

        borrow_requests = BorrowRequest.objects.select_related(
            'book'
        ).filter(
            user=request.user
        ).order_by('-requested_at')

        serializer = BorrowRequestListSerializer(
            borrow_requests,
            many=True
        )

        return success_response(
            message="Borrow requests fetched successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )
    



from django.utils import timezone



class BorrowApproveView(APIView):

    permission_classes = [IsAuthenticated, IsLibrarian]

    def patch(self, request, pk):

        borrow_request = get_object_or_404(BorrowRequest, pk=pk)

        # business rule check
        if borrow_request.status != BorrowRequest.Status.PENDING:

            return error_response(
                message="Invalid action",
                errors={
                    "status": ["Only pending requests can be approved"]
                },
                status_code=400
            )

        borrow_request.status = BorrowRequest.Status.APPROVED
        borrow_request.approved_at = timezone.now()
        borrow_request.save()

        return success_response(
            message="Borrow request approved",
            data={"status": borrow_request.status},
            status_code=200
        )
    
class BorrowRejectView(APIView):

    permission_classes = [IsAuthenticated, IsLibrarian]

    def patch(self, request, pk):

        borrow_request = get_object_or_404(BorrowRequest, pk=pk)

        if borrow_request.status != BorrowRequest.Status.PENDING:

            return error_response(
                message="Invalid action",
                errors={
                    "status": ["Only pending requests can be rejected"]
                },
                status_code=400
            )

        borrow_request.status = BorrowRequest.Status.REJECTED
        borrow_request.save()

        return success_response(
            message="Borrow request rejected",
            data={"status": borrow_request.status},
            status_code=200
        )


class BorrowReturnView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsLibrarian
    ]

    def patch(self, request, pk):

        borrow_request = get_object_or_404(
            BorrowRequest.objects.select_related('book'),
            pk=pk
        )

        # RULE 1: Only APPROVED can be returned
        if borrow_request.status != BorrowRequest.Status.APPROVED:

            return error_response(
                message="Invalid action",
                errors={
                    "status": [
                        "Only approved books can be returned"
                    ]
                },
                status_code=400
            )

        # update status
        borrow_request.status = BorrowRequest.Status.RETURNED
        borrow_request.return_at = timezone.now()
        borrow_request.save()

        return success_response(
            message="Book returned successfully",
            data={
                "status": borrow_request.status,
                "return_at": borrow_request.return_at
            },
            status_code=200
        )
    


class BookReviewCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, book_id):

        book = get_object_or_404(Book, pk=book_id)

        if BookReview.objects.filter(
            book=book,
            user=request.user
        ).exists():

            return error_response(
                message="Validation Error",
                errors={
                    "review": ["You already reviewed this book"]
                },
                status_code=status.HTTP_400_BAD_REQUEST
            )

        serializer = BookReviewSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save(
                user=request.user,
                book=book
            )

            return success_response(
                message="Review added successfully",
                data=serializer.data,
                status_code=status.HTTP_201_CREATED
            )

        return error_response(
            message="Validation Error",
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )
    

class BookReviewDetailView(APIView):

    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_object(self, pk):

        return get_object_or_404(BookReview, pk=pk)

    def get(self, request, pk):

        review = self.get_object(pk)

        serializer = BookReviewSerializer(review)

        return success_response(
            message="Review fetched",
            data=serializer.data,
            status_code=200
        )

    








        





