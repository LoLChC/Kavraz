from django.contrib import admin
from .models import products, category,Cart, CartItem

@admin.register(products)
class productsAdmin(admin.ModelAdmin):
    list_display = ("title", "isActive","slug","featured","category")
    list_display_links = ("title","slug",)
    readonly_fields = ("slug",)
    list_filter = ("isActive", "featured",)
    list_editable = ("isActive","featured","category")
    search_fields = ("title","description")

@admin.register(category)
class categoryAdmin(admin.ModelAdmin):
    list_display = ("title", "isActive", "slug",)
    list_editable = ("isActive",)
    list_filter = ("isActive",)
    search_fields = ("title",)
    readonly_fields = ("slug",)

admin.site.register(Cart)
admin.site.register(CartItem)