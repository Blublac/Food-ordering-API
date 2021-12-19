from django.contrib import admin

from order.models import Order

@admin.register(Order)


class Orderadmin(admin.ModelAdmin):
    list_display=["order_no","order","user","status"]
    search_fields = ['order','order_no','user']
