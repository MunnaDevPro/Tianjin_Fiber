# blog/admin.py is disabled to hide the unused Blog section from Django Admin.
# To restore, uncomment the lines below.

# from django.contrib import admin
# from .models import BlogCategory, Post
# 
# @admin.register(BlogCategory)
# class BlogCategoryAdmin(admin.ModelAdmin):
#     prepopulated_fields = {'slug': ('name',)}
#     list_display = ('name', 'is_active', 'order')
# 
# @admin.register(Post)
# class PostAdmin(admin.ModelAdmin):
#     prepopulated_fields = {'slug': ('title',)}
#     list_display = ('title', 'category', 'published_date', 'is_active')
#     list_filter = ('category', 'is_active')
#     search_fields = ('title', 'content')
