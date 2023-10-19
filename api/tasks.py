from datetime import timedelta
from django.utils import timezone

from celery import shared_task

from django.contrib.auth.models import User
from .models import ReadingStatistics, ReadingSession


@shared_task
def update_reading_statistics():
    print("Завантаження даних...")
    users = User.objects.all()
    for user in users:
        # Получаем текущее время
        now = timezone.now()

        # Определяем даты, на которые мы хотим сделать выборку (7 и 30 дней назад)
        seven_days_ago = now - timedelta(days=7)
        thirty_days_ago = now - timedelta(days=30)

        # Фильтруем сеансы чтения для пользователя
        sessions = ReadingSession.objects.filter(user=user, end_time__isnull=False)

        # Фильтруем сеансы чтения за последние 7 дней
        sessions_7_days = sessions.filter(end_time__gte=seven_days_ago, end_time__lte=now)

        # Фильтруем сеансы чтения за последние 30 дней
        sessions_30_days = sessions.filter(end_time__gte=thirty_days_ago, end_time__lte=now)

        # Рассчитываем общее время чтения за 7 и 30 дней
        total_reading_7_days = sum(
            (session.end_time - session.start_time).total_seconds() / 3600 for session in sessions_7_days)
        total_reading_30_days = sum(
            (session.end_time - session.start_time).total_seconds() / 3600 for session in sessions_30_days)

        # Обновляем запись ReadingStatistics для пользователя
        reading_statistics, created = ReadingStatistics.objects.get_or_create(user=user)
        reading_statistics.total_reading_7_days = total_reading_7_days
        reading_statistics.total_reading_30_days = total_reading_30_days
        reading_statistics.save()
