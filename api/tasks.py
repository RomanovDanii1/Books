from datetime import timedelta
from django.utils import timezone

from celery import shared_task

from django.contrib.auth.models import User
from .models import ReadingStatistics, ReadingSession

@shared_task
def update_reading_statistics():
    # Завдання Celery для оновлення статистики читання користувачів

    print("Завантаження даних...")

    # Отримуємо всіх користувачів
    users = User.objects.all()

    for user in users:
        now = timezone.now()  # Поточний час

        # Визначаємо дати для вибірки (7 та 30 днів назад)
        seven_days_ago = now - timedelta(days=7)
        thirty_days_ago = now - timedelta(days=30)

        # Фільтруємо сесії читання для користувача
        sessions = ReadingSession.objects.filter(user=user, end_time__isnull=False)

        # Фільтруємо сесії читання за останні 7 днів
        sessions_7_days = sessions.filter(end_time__gte=seven_days_ago, end_time__lte=now)

        # Фільтруємо сесії читання за останні 30 днів
        sessions_30_days = sessions.filter(end_time__gte=thirty_days_ago, end_time__lte=now)

        # Розраховуємо загальний час читання за 7 та 30 днів
        total_reading_7_days = sum(
            (session.end_time - session.start_time).total_seconds() / 3600 for session in sessions_7_days)
        total_reading_30_days = sum(
            (session.end_time - session.start_time).total_seconds() / 3600 for session in sessions_30_days)

        # Оновлюємо запис в моделі ReadingStatistics для користувача
        reading_statistics, created = ReadingStatistics.objects.get_or_create(user=user)
        reading_statistics.total_reading_7_days = total_reading_7_days
        reading_statistics.total_reading_30_days = total_reading_30_days
        reading_statistics.save()
