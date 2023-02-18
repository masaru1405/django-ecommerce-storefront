from django.contrib import admin

from . import models

#Product
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
   list_display = ['title', 'price', 'inventory_status', 'collection_title']
   list_editable = ['price']
   list_per_page = 10
   list_select_related = ['collection']

   def collection_title(self, product):
      return product.collection.title

   @admin.display(ordering='inventory') #Part 1 - Cap.6 - video 5
   def inventory_status(self, product):
      if product.inventory < 10:
         return 'Low'
      return 'OK'

#Customer
@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
   list_display = ['first_name', 'last_name', 'membership']
   list_editable = ['membership']
   ordering = ['first_name', 'last_name']
   list_per_page = 10

#Order
@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
   list_display = ['id', 'placed_at', 'customer']

#Collection
admin.site.register(models.Collection)

