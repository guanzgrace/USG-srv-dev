from django.contrib import admin
from models import Category, App
from adminsortable.admin import SortableAdmin

class CategoryAdmin(SortableAdmin):
    list_display = ('name',)
    
admin.site.register(Category, CategoryAdmin)

class AppAdmin(SortableAdmin):
    list_display = ('title', 'category', 'slideshow_index',)
    list_editable = ('slideshow_index',)
    list_filter = ('category',)
    ordering = ['category__order', 'order']

admin.site.register(App, AppAdmin)
