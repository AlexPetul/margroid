from django.contrib import admin
from django.urls import path, re_path, include, reverse_lazy
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from margaroid_app.views import *

urlpatterns = [
re_path(r'^$', base_view, name='base_view'),
re_path(r'^showroom/$', showroom_view, name='showroom_view'),
re_path(r'^search/$', search_view, name='search_view'),
re_path(r'^detail-news/(?P<slug>[-\w]+)/$', detail_news_view, name='detail_news_view'),
re_path(r'^news/$', news_view, name='news_view'),
re_path(r'^orders/$', orders_view, name='orders_view'),
re_path(r'^cart/$', cart_view, name='cart_view'),
re_path(r'^make-order/$', make_order_view, name='make_order_view'),
re_path(r'^inc-product-count/$', increase_product_count_view, name='increase_product_count_view'),
re_path(r'^dec-product-count/$', decrease_product_count_view, name='decrease_product_count_view'),
re_path(r'^select-product-color/$', select_product_color_view, name='select_product_color_view'),
re_path(r'^add-complect-to-cart/$', add_complect_to_cart_view, name='add_complect_to_cart_view'),
re_path(r'^add-to-cart/$', add_to_cart_view, name='add_to_cart_view'),
re_path(r'^remove-from-cart/$', remove_from_cart_view, name='remove_from_cart_view'),
re_path(r'^category/(?P<category_slug>[-\w]+)/subcategory/(?P<subcategory_slug>[-\w]+)/$', subcategory_detail_view, name='subcategory_detail_view'),
re_path(r'^components/$', components_view, name='components_view'),
re_path(r'^add-comment/(?P<product_id>\d+)/$', add_comment_view, name='add_comment_view'),
re_path(r'^product/(?P<product_id>\d+)/$', product_detail_view, name='product_detail_view'),
re_path(r'^category/(?P<slug>[-\w]+)/$', category_detail_view, name='category_detail_view'),
re_path(r'^add-to-comparison/$', add_to_comparison_view, name='add_to_comparison_view'),
re_path(r'^delete-from-comparison/$', delete_from_comparison_view, name='delete_from_comparison_view'),
re_path(r'^compare/$', compare_view, name='compare_view'),
re_path(r'^save-profile-info/$', save_profile_info_view, name='save_profile_info_view'),
re_path(r'^profile/$', profile_view, name='profile_view'),
re_path(r'^delivery/$', delivery_view, name='delivery_view'),
re_path(r'^pricelist-print/(?P<slug>[-\w]+)/$', print_pricelist_view, name='print_pricelist_view'),
re_path(r'^price-list/$', pricelist_view, name='pricelist_view'),
re_path(r'^registration/$', registration_view, name='registration_view'),
re_path(r'^send-feedback/$', send_feedback_view, name='send_feedback_view'),
re_path(r'^login/$', login_view, name='login_view'),
re_path(r'^logout/$', LogoutView.as_view(next_page=reverse_lazy('base_view')), name='logout_view'),
re_path('^', include('django.contrib.auth.urls')),
path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)