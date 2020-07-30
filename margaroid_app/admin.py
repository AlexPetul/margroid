from django.contrib import admin
from .models import *
from .forms import ComplectForProductsForm
from django.contrib.admin.views.main import ChangeList


class CategoryAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('name', )}

class CategoryTypeAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('name', )}

class ProductAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('name', )}
	list_display = ('name', 'on_sale', 'in_stock', 'category')
	form = ComplectForProductsForm

class NewsAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('title', )}

class ShopUserAdmin(admin.ModelAdmin):
	list_display = ('user', 'get_user_email', 'get_discount', 'phone_number')

	def get_user_email(self, obj):
		return obj.user.email
	get_user_email.short_description = 'Почта'

	def get_discount(self, obj):
		return "{0} %".format(obj.discount)
	get_discount.short_description = 'Скидка'


class SizesAdmin(admin.ModelAdmin):
	list_display = ('product', 'get_size', 'price', )

	def get_size(self, obj):
		return "{0}*{1}".format(obj.height, obj.width)
	get_size.short_description = 'Размер'


admin.site.register(Category, CategoryAdmin)
admin.site.register(CategoryType, CategoryTypeAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(ShopUser, ShopUserAdmin)
admin.site.register(Comment)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Sizes, SizesAdmin)
admin.site.register(Colors)
admin.site.register(StandartSale)
admin.site.register(Order)
admin.site.register(OrderItems)
admin.site.register(DeliveryType)
admin.site.register(ProductColorsSizes)
