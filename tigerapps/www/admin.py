from django.contrib import admin
from models import Category, App

class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': ('name',)
        }),
    ]
    
    readonly_fields = ('index',)
    list_display = ('id', 'name', 'index',)
    
    def save_model(self, request, obj, form, change):
        obj.index = Category.objects.all().count()
        obj.save()


class AppAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': ('name', 'abbr_name', 'url', 'icon', 'description',)
        }),
        ('Placement', {
            'fields': ('category', 'slideshow_picture',)
        }),
    ]
    
    readonly_fields = ('slideshow_index', 'category_index',)
    list_display = ('id', 'name', 'category', 'category_index', 'slideshow_index',)
    list_filter = ('category',)

    def save_model(self, request, obj, form, change):
        obj.category_index = App.objects.filter(category=obj.category).count()
        obj.save()

admin.site.register(Category, CategoryAdmin)
admin.site.register(App, AppAdmin)
