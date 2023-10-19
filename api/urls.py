from django.urls import path, include
from .views import *

urlpatterns = [
    path('add/', AddBookView.as_view(), name='add-book'),
    path('books/', BookList.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetail.as_view(), name='book-detail'),
    path('start-reading/', StartReadingView.as_view(), name='start-reading'),
    path('end-reading/', EndReadingView.as_view(), name='end-reading'),
    path('sessions/', ReadingSessionsView.as_view(), name='sessions'),
    path('auth/', include('rest_framework.urls'), name='authorization')
]
