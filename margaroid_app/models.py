from django.db import models
from decimal import Decimal
from django.conf import settings


class ShopUser(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
	phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name='Телефон')
	discount = models.PositiveSmallIntegerField(default=0, blank=True, verbose_name='Скидка')

	def __str__(self):
		return self.user.username

	class Meta:
		verbose_name_plural = 'Пользователи'


class CategoryType(models.Model):
	name = models.CharField(max_length=100)
	image = models.ImageField(upload_to='category_images', null=True)
	slug = models.SlugField(max_length=100)

	class Meta:
		verbose_name_plural = 'Подкатегории'

	def __str__(self):
		return self.name


class Category(models.Model):
	name = models.CharField(max_length=100)
	image = models.ImageField(upload_to='category_images', null=True)
	slug = models.SlugField(max_length=100)
	subtype = models.ManyToManyField(CategoryType, blank=True)

	class Meta:
		verbose_name_plural = 'Категории'

	def __str__(self):
		return self.name


class News(models.Model):
	title = models.CharField(max_length=200, verbose_name='Заголовок')
	slug = models.SlugField(max_length=200, verbose_name='(Ссылка)', blank=True)
	content = models.TextField(max_length=3000, verbose_name='Содержимое')
	timestamp = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name_plural = 'Новости'

	def __str__(self):
		return self.title


class Product(models.Model):
	name = models.CharField(max_length=200, verbose_name='Имя')
	slug = models.SlugField(max_length=200, verbose_name='(Ссылка)', blank=True)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
	sub_category = models.ForeignKey(CategoryType, on_delete=models.CASCADE, null=True, verbose_name='Подкатегория', blank=True)
	image = models.ImageField(upload_to='product_images', null=True, verbose_name='Изображение')
	vendor_code = models.CharField(max_length=100, verbose_name='Артикул', blank=True)
	in_stock = models.PositiveIntegerField(default=0, verbose_name='Наличие (шт)')
	complect = models.ManyToManyField('Product', verbose_name='Комплектующие', blank=True)
	price = models.PositiveIntegerField(null=True, verbose_name='Цена')
	description = models.CharField(max_length=2000, verbose_name='Описание')
	on_sale = models.BooleanField(default=False, blank=True, verbose_name='На скидке')
	sale = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name='Размер скидки')
	new_price = models.PositiveIntegerField(blank=True, null=True, verbose_name='Новая цена')
	colors = models.ManyToManyField('Colors', blank=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	@property
	def get_new_price(self):
		new_price = self.price
		if self.on_sale:
			new_price = self.price * Decimal(1 - self.sale/100)
		return new_price

	def save(self, *args, **kwargs):
		self.new_price = self.get_new_price
		super(Product, self).save(*args, **kwargs)

	class Meta:
		verbose_name_plural = 'Товары'

	def __str__(self):
		return self.name


class Sizes(models.Model):
	product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Продукт')
	height = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Высота')
	width = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Ширина')
	price = models.PositiveIntegerField(default=0, verbose_name='Цена')

	class Meta:
		verbose_name_plural = 'Размеры'

	def __str__(self):
		return "{0} ({1}*{2})".format(self.product.name, self.height, self.width)


class CartItem(models.Model):
	product = models.ForeignKey(Sizes, on_delete=models.CASCADE, null=True)
	count = models.PositiveSmallIntegerField(default=1)
	color = models.CharField(max_length=100, blank=True, null=True)
	price_per_item_color = models.PositiveIntegerField(default=0, null=True, blank=True)
	total_price = models.PositiveIntegerField(default=0)

	class Meta:
		verbose_name_plural = 'Товары в корзине'

	def __str__(self):
		return self.product.product.name


class Colors(models.Model):
	name = models.CharField(max_length=100, verbose_name='Название')
	image = models.ImageField(upload_to='product_colors', null=True, verbose_name='Изображение')
	price = models.PositiveIntegerField(default=3000, verbose_name='Цена')

	class Meta:
		verbose_name_plural = 'Цвета'

	def __str__(self):
		return self.name


class Cart(models.Model):
	products = models.ManyToManyField(CartItem, blank=True)
	total_price = models.PositiveIntegerField(default=0)

	class Meta:
		verbose_name_plural = 'Корзины'

	def __str__(self):
		return '%s%d' % ('Cart', self.id)

	def add_to_cart(self, product, color=None, default_count=1):
		cart = self
		new_item, _ = CartItem.objects.get_or_create(product=product, count=default_count, total_price=product.price * default_count)
		if new_item not in cart.products.all():
			if not color is None:
				new_item.color = color.color.name
				new_item.total_price = color.price * default_count
				new_item.price_per_item_color = color.price
				new_item.save()
			cart.products.add(new_item)
			cart.total_price += new_item.total_price
			cart.save()

	def remove_from_cart(self, product):
		cart = self
		for cart_item in cart.products.all():
			if cart_item.product == product:
				cart.products.remove(cart_item)
				cart_item.delete()
				cart.total_price -= cart_item.total_price
				cart.save()


class StandartSale(models.Model):
	sale = models.PositiveSmallIntegerField(default=0, verbose_name='Стандартная скидка')

	def __str__(self):
		return "{0} %".format(self.sale)

	class Meta:
		verbose_name_plural = 'Стандартная скидка'


class Comment(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	user = models.ForeignKey(ShopUser, on_delete=models.CASCADE, null=True)
	body = models.TextField()
	created_on = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name_plural = 'Комментарии'

	def __str__(self):
		return "Комментарий к продукту {0} от {1}".format(self.product.name, self.user.user.username)


class OrderItems(models.Model):
	order = models.ForeignKey('Order', on_delete=models.CASCADE, null=True)
	product = models.ForeignKey(Sizes, on_delete=models.CASCADE, null=True)
	count = models.PositiveSmallIntegerField(default=1)
	color = models.CharField(max_length=100, blank=True, null=True)
	total_price = models.PositiveIntegerField(default=0)
	

class DeliveryType(models.Model):
    image = models.ImageField(upload_to='delivery_images', verbose_name='Изображение')
    description = models.CharField(max_length=1000, verbose_name='Описание')
    
    class Meta:
        verbose_name_plural = 'Информация о доставке'
        
    def __str__(self):
        return "Доставка {0}".format(self.id)


class ProductColorsSizes(models.Model):
	product = models.ForeignKey(Sizes, on_delete=models.CASCADE, verbose_name='Продукт (с размером)')
	color = models.ForeignKey(Colors, on_delete=models.CASCADE, verbose_name='Цвет')
	price = models.PositiveIntegerField(default=0, verbose_name='Цена')

	class Meta:
		verbose_name_plural = 'Цены цветов'

	def __str__(self):
		return "{0} - {1}".format(self.product.product.name, self.color.name)


class Order(models.Model):
	user = models.ForeignKey(ShopUser, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Пользователь')
	name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Имя')
	full_name = models.CharField(max_length=200, blank=True, null=True, verbose_name='ФИО')
	phone = models.CharField(max_length=30, blank=True, null=True, verbose_name='Телефон')
	email = models.CharField(max_length=150, blank=True, null=True, verbose_name='Почта')
	delivery_type = models.CharField(max_length=50, blank=True, null=True, verbose_name='Способ доставки')
	delivery_region = models.CharField(max_length=100, blank=True, null=True, verbose_name='Регион')
	delivery_city = models.CharField(max_length=100, blank=True, null=True, verbose_name='Город')
	delivery_street = models.CharField(max_length=100, blank=True, null=True, verbose_name='Улица')
	delivery_house = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Номер дома')
	delivery_padik = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Номер подъезда')
	delivery_flat = models.PositiveIntegerField(blank=True, null=True, verbose_name='Квартира')
	delivery_deadline = models.CharField(max_length=100, blank=True, null=True, verbose_name='Сроки')
	take_away_address = models.CharField(max_length=100, blank=True, null=True, verbose_name='Адрес при самовывозе')
	transport_company_address = models.CharField(max_length=100, blank=True, null=True, verbose_name='Адрес транспортной компании')
	payment_type = models.CharField(max_length=50, blank=True, null=True, verbose_name='Тип оплаты')
	org_name = models.CharField(max_length=200, blank=True, null=True, verbose_name='Наименование организации')
	inn = models.CharField(max_length=20, blank=True, null=True, verbose_name='ИНН')
	legal_address = models.CharField(max_length=100, blank=True, null=True, verbose_name='Юридический адрес')
	additional_information = models.TextField(blank=True, null=True, verbose_name='Дополнительная информация')
	STATUS_TYPES = (
		('Оформлен', 'Оформлен'),
		('Выполнен', 'Выполнен'),
		('Доставлен', 'Доставлен'),
		('Отменен', 'Отменен'),
		('Выдан', 'Выдан')
	)
	status = models.CharField(max_length=20, choices=STATUS_TYPES, default='Оформлен')
	total_price = models.PositiveIntegerField(default=0)
	timestamp = models.DateTimeField(auto_now_add=True)
	


	class Meta:
		verbose_name_plural = 'Заказы'

	def __str__(self):
		return "Заказ №{0}".format(self.id)