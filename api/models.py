from datetime import datetime
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publication_year = models.PositiveIntegerField(null=True, default=None)
    short_description = models.TextField()
    full_description = models.TextField()
    last_read_date = models.DateTimeField(null=True, blank=True, default=None)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        current_year = datetime.now().year
        if not isinstance(self.publication_year, int):
            raise ValueError("publication_year має бути цілим числом")
        if self.publication_year > current_year:
            raise ValueError("publication_year не може бути у майбутньому")
        super(Book, self).save(*args, **kwargs)

class ReadingSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.user is None or self.book is None:
            raise ValueError("Обидва поля 'user' та 'book' повинні бути задані для валідного сеансу читання")
        if self.start_time > self.end_time:
            raise ValueError("end_time повинен бути більше, ніж start_time")
        super().save(*args, **kwargs)

class BookReadingTime(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    books = models.JSONField(default=dict)
    total_reading_time = models.FloatField(default=0.0)
    total_session_counter = models.IntegerField(default=0)

@receiver(pre_save, sender=BookReadingTime)
def validate_book_reading_time(sender, instance, **kwargs):
    if not instance.user:
        raise ValueError("Поле 'user' повинно бути заповненим для створення запису 'BookReadingTime'")

    if not isinstance(instance.books, dict) or not all(
        isinstance(val, dict) and
        "reading_time" in val and isinstance(val["reading_time"], int) and
        "session_counter" in val and isinstance(val["session_counter"], int)
        for val in instance.books.values()
    ):
        raise ValueError("Невірний формат даних для 'books' в 'BookReadingTime'")

@receiver(post_save, sender=ReadingSession)
def update_book_reading_time(sender, instance, created, **kwargs):
    if not created:
        user = instance.user
        book = instance.book
        reading_time = (instance.end_time - instance.start_time).total_seconds()
        book_reading_time, created = BookReadingTime.objects.get_or_create(user=user)
        books_info = book_reading_time.books

        if str(book.id) not in books_info:
            books_info[str(book.id)] = {
                "reading_time": 0,
                "session_counter": 0,
            }

        books_info[str(book.id)]["reading_time"] += reading_time
        books_info[str(book.id)]["session_counter"] += 1

        book_reading_time.total_reading_time = sum(book_info["reading_time"] for book_info in books_info.values())
        book_reading_time.total_session_counter = sum(book_info["session_counter"] for book_info in books_info.values())

        book_reading_time.save()

class ReadingStatistics(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_reading_7_days = models.FloatField(default=0.0)
    total_reading_30_days = models.FloatField(default=0.0)

@receiver(pre_save, sender=ReadingStatistics)
def validate_reading_statistics(sender, instance, **kwargs):
    if not isinstance(instance.total_reading_7_days, (int, float)) or not isinstance(instance.total_reading_30_days, (int, float)):
        raise ValueError("Невірний формат даних для 'total_reading_7_days' або 'total_reading_30_days' в 'ReadingStatistics'")

    if instance.total_reading_7_days < 0 or instance.total_reading_30_days < 0:
        raise ValueError("'total_reading_7_days' та 'total_reading_30_days' мають бути не від'ємними в 'ReadingStatistics'")
