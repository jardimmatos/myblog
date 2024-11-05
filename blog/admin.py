from django.contrib import admin
from . import models


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'published', 'status')
    list_filter = ('status',)
    prepopulated_fields = {'slug': ('title',)}
    save_as = True
    date_hierarchy = 'published'

    def save_model(self, request, obj, form, change):
        """
        Registrar usuário que criou o post via admin
        """
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)