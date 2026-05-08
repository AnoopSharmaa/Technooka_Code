from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from LMS.views import BookDetailView, BookReviewCreateView, BorrowRequestView, BorrowReturnView, GenreView, RegisterView, BookView,AuthorView,BorrowApproveView,BorrowRejectView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('books/', BookView.as_view(), name='book_view'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('authors/', AuthorView.as_view(), name='author_view'),
    path('genres/', GenreView.as_view(), name='genre_view'),
    path('borrow/', BorrowRequestView.as_view(), name='borrow_request'),
    path('borrow/<int:pk>/approved/', BorrowApproveView.as_view(), name='borrow_approve'),
    path('borrow/<int:pk>/rejected/', BorrowRejectView.as_view(), name='borrow_reject'),
    path('borrow/<int:pk>/returned/', BorrowReturnView.as_view(), name='borrow_returned'),
    path('books/<int:pk>/reviews/', BookReviewCreateView.as_view(), name='book_reviews'),

]