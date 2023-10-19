from rest_framework import generics
from .serializers import *
from .tasks import *

class AddBookView(generics.CreateAPIView):
    # Додає книгу до бази даних
    queryset = Book.objects.all()
    serializer_class = AddBookSerializer

class BookList(generics.ListAPIView):
    # Повертає список всіх книг
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookDetail(generics.RetrieveAPIView):
    # Повертає деталі однієї книги
    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer

class ReadingSessionsView(generics.ListAPIView):
    # Повертає список сесій читання
    queryset = ReadingSession.objects.all()
    serializer_class = ReadingSessionSerializer

class StartReadingView(generics.CreateAPIView):
    # Розпочинає нову сесію читання
    queryset = ReadingSession.objects.all()
    serializer_class = ReadingSessionSerializer

    def perform_create(self, serializer):
        # Завершує активну сесію, якщо вона існує, та створює нову
        user_id = self.request.data.get('user')
        user = User.objects.get(id=user_id)
        active_session = ReadingSession.objects.filter(user=user, end_time__isnull=True).first()
        if active_session:
            active_session.end_time = timezone.now()
            active_session.save()
        serializer.save(user=user, start_time=timezone.now())

class EndReadingView(generics.CreateAPIView):
    # Завершує активну сесію читання
    queryset = ReadingSession.objects.all()
    serializer_class = ReadingSessionSerializer

    def perform_create(self, serializer):
        # Завершує активну сесію, якщо вона існує
        user_id = self.request.data.get('user')
        user = User.objects.get(id=user_id)
        active_session = ReadingSession.objects.filter(user=user, end_time__isnull=True).first()
        if active_session:
            active_session.end_time = timezone.now()
            active_session.save()
