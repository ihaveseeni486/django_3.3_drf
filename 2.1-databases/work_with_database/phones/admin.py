from django.contrib import admin
from .models import Phone


class PhoneAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image', 'price', 'release_date', 'lte_exists', 'slug')
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Phone, PhoneAdmin)

