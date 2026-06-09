from django.contrib.admin import register, ModelAdmin

from airbox.filesystem.models import Folder, File


@register(Folder)
class FolderAdmin(ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@register(File)
class FileAdmin(ModelAdmin):
    list_display = ('folder__name', 'name',)
    search_fields = ('folder__name', 'name',)
