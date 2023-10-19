import pytest
from api.models import *
from datetime import datetime, timedelta

from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError


@pytest.mark.django_db
class TestBookModel:
    # Тести для моделі Book
    @pytest.mark.parametrize("test_data", [
        {
            "title": "",
            "author": "",
            "publication_year": "dsas", # Помилка: рік видання має бути числом
            "short_description": "Short description 1",
            "full_description": "Full description 1",
        },
        {
            "title": "Test Book 2",
            "author": "Author 2",
            "publication_year": 2025, # Помилка: рік видання не може бути у майбутньому
            "short_description": "",
            "full_description": "Full description 2",
        },
        # Добавьте дополнительные наборы параметров, если необходимо
    ])
    # Тест на створення об'єкта моделі Book та перевірку валідації даних
    def test_create_book(self, test_data):
        if not isinstance(test_data["publication_year"], int):
            with pytest.raises(ValueError):
                Book.objects.create(**test_data)
        else:
            current_year = datetime.now().year
            if test_data["publication_year"] > current_year:
                with pytest.raises(ValueError):
                    Book.objects.create(**test_data)
            else:
                book = Book.objects.create(**test_data)
                for field, expected_value in test_data.items():
                    assert getattr(book, field) == expected_value

    # Тести для моделі ReadingSession
    @pytest.mark.parametrize("test_data", [
        {  # Валідна сесія читання
            "user": None,
            "book": None,
            "start_time": datetime.now(),
            "end_time": datetime.now() + timedelta(hours=1),
        },
        {  # Помилка: end_time менше start_time
            "user": None,
            "book": None,
            "start_time": datetime.now(),
            "end_time": datetime.now() - timedelta(hours=1),
        },
    ])
    def test_create_reading_session(self, test_data):
        # Тест на створення об'єкта моделі ReadingSession та перевірку валідації даних
        def test_create_reading_session(self, test_data):
            if test_data["user"] is None or test_data["book"] is None:
                with pytest.raises(ValueError):
                    ReadingSession.objects.create(
                        user=test_data["user"],
                        book=test_data["book"],
                        start_time=test_data["start_time"],
                        end_time=test_data["end_time"]
                )
            if test_data["start_time"] > test_data["end_time"]:
                with pytest.raises(ValidationError):
                    ReadingSession.objects.create(
                        user=test_data["user"],
                        book=test_data["book"],
                        start_time=test_data["start_time"],
                        end_time=test_data["end_time"]
                    )

    # Тести для моделі BookReadingTime
    @pytest.mark.parametrize("test_data", [
        {   # Валідні дані
            "user": "test_user",
            "books": {"1": {"reading_time": 100, "session_counter": 5}},
            "total_reading_time": 0.0,
            "total_session_counter": 0,
        },
        {  # Помилка: невірний тип даних для books
            "user": "another_user",
            "books": "invalid_data", # Помилка: books має бути словником
            "total_reading_time": 0.0,
            "total_session_counter": 0,
        },

    ])
    # Тест на створення об'єкта моделі BookReadingTime та перевірку валідації даних
    def test_create_book_reading_time(self, test_data):
        if test_data["user"] is None:
            with pytest.raises(ValueError):
                BookReadingTime.objects.create(
                    user=test_data["user"],
                    books=test_data.get("books", {}),
                    total_reading_time=test_data.get("total_reading_time", 0.0),
                    total_session_counter=test_data.get("total_session_counter", 0)
                )
        if not isinstance(test_data["books"], dict) or not all(
            isinstance(val, dict) and
            "reading_time" in val and isinstance(val["reading_time"], int) and
            "session_counter" in val and isinstance(val["session_counter"], int)
            for val in test_data["books"].values()
        ):
            with pytest.raises(ValueError):
                BookReadingTime.objects.create(
                    user=test_data["user"],
                    books=test_data.get("books", {}),
                    total_reading_time=test_data.get("total_reading_time", 0.0),
                    total_session_counter=test_data.get("total_session_counter", 0)
                )

    # Тести для моделі ReadingStatistics
    @pytest.mark.parametrize("test_data", [
        {
            "user": "first_user",
            "total_reading_7_days": 100.0,
            "total_reading_30_days": 150.0,
        },
        {
            "user": "test_user",
            "total_reading_7_days": 100.0,
            "total_reading_30_days": 150.0,
        },
        {
            "user": "another_user",
            "total_reading_7_days": "invalid_data",  # Помилка: неправильний тип даних
            "total_reading_30_days": 150.0,
        },
        {
            "user": "user_with_data",
            "total_reading_7_days": 100.0,
            "total_reading_30_days": 200.0,
        },
    ])
    def test_create_reading_statistics(self, test_data):
        user = User.objects.create_user(username=test_data["user"], password='test_password')

        if isinstance(test_data["total_reading_7_days"], (int, float)) and isinstance(
                test_data["total_reading_30_days"], (int, float)):
            reading_stats = ReadingStatistics.objects.create(
                user=user,
                total_reading_7_days=test_data["total_reading_7_days"],
                total_reading_30_days=test_data["total_reading_30_days"]
            )
            assert reading_stats.user == user
            assert reading_stats.total_reading_7_days == test_data["total_reading_7_days"]
            assert reading_stats.total_reading_30_days == test_data["total_reading_30_days"]
        else:
            with pytest.raises(ValueError):
                ReadingStatistics.objects.create(
                    user=user,
                    total_reading_7_days=test_data["total_reading_7_days"],
                    total_reading_30_days=test_data["total_reading_30_days"]
                )