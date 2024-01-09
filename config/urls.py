from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = 'Модуль администратора СБЕР кафе'
admin.site.index_title = 'Модуль администратора'
admin.site.site_title = 'СБЕР кафе'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('staff/', include('staff.urls')),
    path('', include('shop.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)