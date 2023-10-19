from rest_framework import serializers
from .models import *


class AddBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('title', 'author', 'publication_year', 'short_description', 'full_description')


class BookDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class CalculateReadingStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookReadingTime
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('title', 'author', 'publication_year', 'short_description')


class ReadingSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingSession
        fields = '__all__'



class BookReadingTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookReadingTime
        fields = '__all__'



