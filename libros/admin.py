from django.contrib import admin
from .models import Book, DeweyCode

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'dewey_code', 'status')
    list_filter = ('status', 'dewey_code')
    search_fields = ('title', 'author', 'isbn')

@admin.register(DeweyCode)
class DeweyCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'description')
    search_fields = ('code', 'description')
