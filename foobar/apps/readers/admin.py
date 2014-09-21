from django.contrib import admin
from .models import Category, Feed

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'position', 'updated_time',)
    ordering = ['position', '-created_time']
    list_filter = ['updated_time']
    
admin.site.register(Category, CategoryAdmin)

class FeedAdmin(admin.ModelAdmin):
    list_display = ('title', 'updated_time',)
    list_filter = ['updated_time']
    
admin.site.register(Feed, FeedAdmin)