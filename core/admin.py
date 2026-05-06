from django.contrib import admin
from .models import InstrumentStack, XyloKey, Song


class XyloKeyInline(admin.TabularInline):
    model = XyloKey
    extra = 8 # Default to 8 keys for a standard xylophone

@admin.register(InstrumentStack)
class InstrumentStackAdmin(admin.ModelAdmin):
    inlines = [XyloKeyInline]
    list_display = ('title', 'owner', 'created_at')

admin.site.register(Song)