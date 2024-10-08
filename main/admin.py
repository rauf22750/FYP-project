
from django.contrib import admin
from .models import Category,Brand,Color,Product,ProductAttribute,Cartview,CartOrderItems,ProductReview,UserAddressBook



class CategoryAdmin(admin.ModelAdmin):
	list_display=('title','image_tag')
admin.site.register(Category,CategoryAdmin)

class brandAdmin(admin.ModelAdmin):
	list_display=('title','image')
admin.site.register(Brand,brandAdmin)

class ColorAdmin(admin.ModelAdmin):
	list_display=('title','color_bg')
admin.site.register(Color,ColorAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display=('id','title','category','brand','status','is_featured')
    list_editable=('status','is_featured')
admin.site.register(Product,ProductAdmin)

# Product Attribute
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display=('id','image_tag','product','price','color')
admin.site.register(ProductAttribute,ProductAttributeAdmin)

# Order
class CartviewAdmin(admin.ModelAdmin):
	list_display=('user','product','quantity','total_price','data_add')
admin.site.register(Cartview,CartviewAdmin)

class CartOrderItemsAdmin(admin.ModelAdmin):
	list_display=('invoice_no','item','image_tag','qty','price','total')
admin.site.register(CartOrderItems,CartOrderItemsAdmin)


class ProductReviewAdmin(admin.ModelAdmin):
	list_display=('user','product','review_text','get_review_rating')
admin.site.register(ProductReview,ProductReviewAdmin)


class UserAddressBookAdmin(admin.ModelAdmin):
	list_display=('user','address','status')
admin.site.register(UserAddressBook,UserAddressBookAdmin)





