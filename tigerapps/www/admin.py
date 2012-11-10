from django.contrib import admin
from models import Category, App
from adminsortable.admin import SortableAdmin


class CategoryAdmin(SortableAdmin):
    fieldsets = [
        (None, {
            'fields': ('name',)
        }),
    ]
    list_display = ('name',)

class AppAdmin(SortableAdmin):
    fieldsets = [
        (None, {
            'fields': ('name', 'abbr_name', 'url', 'icon', 'description',)
        }),
        ('Placement', {
            'fields': ('category', 'slideshow_picture', 'slideshow_index',)
        }),
    ]
    list_display = ('name', 'category', 'slideshow_index',)
    list_editable = ('slideshow_index',)
    list_filter = ('category',)
    ordering = ['category__order', 'order']

admin.site.register(Category, CategoryAdmin)
admin.site.register(App, AppAdmin)
