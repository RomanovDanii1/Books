from django.contrib import admin
from .models import *

class ReadingSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'start_time', 'end_time')
    list_filter = ('user', 'book')

class BookReadingTimeAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_reading_time', 'total_session_counter')
    list_filter = ('user',)

    def total_reading_time(self, obj):
        return obj.total_reading_time
    total_reading_time.short_description = 'Total Reading Time'

    def total_session_counter(self, obj):
        return obj.total_session_counter
    total_session_counter.short_description = 'Total Session Counter'


class ReadingStatisticsAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_reading_7_days', 'total_reading_30_days')

admin.site.register(ReadingSession, ReadingSessionAdmin)
admin.site.register(Book)
admin.site.register(BookReadingTime, BookReadingTimeAdmin)
admin.site.register(ReadingStatistics, ReadingStatisticsAdmin)
