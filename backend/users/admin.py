from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'first_name',
        'last_name',
        'email',
        'role',
        'date_joined'
    )
    search_fields = ('text', 'email')
    list_filter = ('date_joined',)


admin.site.register(User, UserAdmin)
