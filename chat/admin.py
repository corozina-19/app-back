from django.contrib import admin

# Register your models here.
from chat.models import Message, Thread

admin.site.register(Thread)
admin.site.register(Message)
