from django.contrib import admin
from .models import Model, Make, Review, Car


class ModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'make')


class CarAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'avg_rating')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('car', 'rating', 'review_datetime',)


admin.site.register(Make)
admin.site.register(Model, ModelAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Car, CarAdmin)
