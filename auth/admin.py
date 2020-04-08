from django.contrib import admin
from django.contrib.auth.models import User

from auth.models import SocialNetwork


class SocialNetworkInline(admin.TabularInline):
    model = SocialNetwork


class UserAdmin(admin.ModelAdmin):
    inlines = (SocialNetworkInline, )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
