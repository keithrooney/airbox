from django.contrib.admin import register, ModelAdmin

from airbox.iam.models import User


@register(User)
class UserAdmin(ModelAdmin):
    list_display = ('email',)
    search_fields = ('email',)
