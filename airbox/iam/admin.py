from django.contrib.admin import register, ModelAdmin

from airbox.iam.models import User, Organisation, Member


@register(User)
class UserAdmin(ModelAdmin):
    list_display = ('email',)
    search_fields = ('email',)


@register(Organisation)
class OrganisationAdmin(ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@register(Member)
class MemberAdmin(ModelAdmin):
    list_display = ('user__email',)
    search_fields = ('user__email',)
