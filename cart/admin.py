from django.contrib import admin

# Register your models here.
from .models import Order, Item, CheckoutFeedback
admin.site.register(Order)
admin.site.register(Item)

# NEW
@admin.register(CheckoutFeedback)
class CheckoutFeedbackAdmin(admin.ModelAdmin):
	list_display = ("id", "name", "comment", "date")
	ordering = ("-date",)
	search_fields = ("name", "comment")