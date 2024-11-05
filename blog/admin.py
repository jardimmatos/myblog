from django.contrib import admin
from . import models


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_at', 'status')
    list_filter = ('status',)
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    save_as = True
    date_hierarchy = 'created_at'
    raw_id_fields = ('created_by',)

    def save_model(self, request, obj, form, change):
        """
        Registrar usuário que criou o post via admin
        """
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)