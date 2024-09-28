from django.contrib import admin
from pb_app.models import *

# Register your models here.
admin.site.register(LibraryUser)
admin.site.register(Books)
admin.site.register(FavouriteCollections)
admin.site.register(Rating)