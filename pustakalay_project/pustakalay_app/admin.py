from django.contrib import admin
from pustakalay_app.models import *

# Register your models here.
admin.site.register(LibraryUser)
admin.site.register(Books)
admin.site.register(FavouritiesBooks)
admin.site.register(Rating)