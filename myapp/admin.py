from django.contrib import admin
from myapp.models import Product,Cart,Buy,Reply,Category,FAQ,ContactMessage
# Register your models here.
admin.site.register(Product)
admin.site.register(Cart) 
admin.site.register(Buy)
admin.site.register(Reply)
admin.site.register(Category)
admin.site.register(FAQ)
admin.site.register(ContactMessage)


