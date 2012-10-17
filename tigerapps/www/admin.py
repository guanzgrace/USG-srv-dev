from django.contrib import admin
from models import Category, App
from adminsortable.admin import SortableAdmin

class CategoryAdmin(SortableAdmin):
    list_display = ('name',)
    
    def save_model(self, request, obj, form, change):
        obj.index = Category.objects.all().count()
        obj.save()

admin.site.register(Category, CategoryAdmin)

class AppAdmin(SortableAdmin):
    list_display = ('title', 'category', 'slideshow_index',)
    list_editable = ('slideshow_index',)
    list_filter = ('category',)
    ordering = ['category__order', 'order']

    def save_model(self, request, obj, form, change):
        obj.category_index = App.objects.filter(category=obj.category).count()
        obj.save()

admin.site.register(App, AppAdmin)
