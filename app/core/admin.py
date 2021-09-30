from django.contrib import admin
from .models import Model, Make, Review, Car


class CarAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'avg_rating')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('car', 'rating', 'review_datetime',)


admin.site.register(Model)
admin.site.register(Make)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Car, CarAdmin)
