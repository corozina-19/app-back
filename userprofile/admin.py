from django.contrib import admin

from userprofile.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    #   raw_id_fields = ('user',)
    pass
