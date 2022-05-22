from django.contrib import admin
from .models import BlogEntry, EntryComment


admin.site.register(BlogEntry)
admin.site.register(EntryComment)
