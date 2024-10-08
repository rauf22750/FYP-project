"""
URL configuration for practice project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from practice import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/',views.signaction,name='signup'),
    path('login/',views.loginuser,name='login'),
    path('',views.welcomepage,name='welcome'),
    path('about/',views.about,name='about'),
    path('category/',views.category,name='category'),
    path('category_product_list/<int:cat_id>',views.category_product_list,name='category_product_list'),
    path('brand_product_list/<int:brand_id>',views.brand_product_list,name='brand_product_list'),
    path('load-more-data',views.load_more_data,name='load_more_data'),
    path('brand/',views.brand,name='brand'),
    path('product/',views.product,name='product'),
    path('product/<str:slug>/<int:id>',views.product_detail,name='product_detail'),
    path('form/',views.form,name='form'),
    path('save-review/<int:pid>',views.save_review, name='save-review'),
    path('filter-data',views.filter_data,name='filter_data'),
    path('profile/', views.profile, name='profile'),
    path('signout',views.signout, name='logout'),
    path('add-to-cart',views.add_to_cart,name='add_to_cart'),
    path('cart',views.cart_view,name='cart_view'),
    # path('delete-from-cart',views.delete_cart_item,name='delete-from-cart'),
    # path('update-cart',views.update_cart_item,name='update-cart'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)