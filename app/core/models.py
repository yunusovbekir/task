from functools import cached_property

from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import CustomManager


class Make(models.Model):
    title = models.CharField(
        _('title'),
        max_length=255,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Make")
        verbose_name_plural = _("Makes")
        ordering = ('title',)


class Model(models.Model):
    make = models.ForeignKey(
        'core.Make',
        on_delete=models.CASCADE,
        verbose_name=_('make'),
        related_name='models',
    )
    title = models.CharField(
        _('title'),
        max_length=255,
    )

    def __str__(self):
        return f'{self.make.title} - {self.title}'

    class Meta:
        verbose_name = _("Model")
        verbose_name_plural = _("Models")
        ordering = ('title',)


class RatingChoices(models.IntegerChoices):
    VERY_BAD = 1
    BAD = 2
    POOR = 3
    GOOD = 4
    EXCELLENT = 5


class Review(models.Model):
    car = models.ForeignKey(
        'core.Car',
        on_delete=models.CASCADE,
        verbose_name=_('car'),
        related_name='reviews',
    )
    rating = models.IntegerField(
        _('rating'),
        choices=RatingChoices.choices,
    )
    review_datetime = models.DateTimeField(
        _('review add datetime'),
        auto_now_add=True,
    )
    objects = CustomManager()

    def __str__(self):
        return f"Review for {self.car}"

    class Meta:
        verbose_name = _('Review')
        verbose_name_plural = _('Reviews')
        ordering = ('-review_datetime',)


class Car(models.Model):
    make = models.ForeignKey(
        'core.Make',
        on_delete=models.CASCADE,
        verbose_name=_("make"),
        related_name='cars',
    )
    model = models.ForeignKey(
        'core.Model',
        on_delete=models.CASCADE,
        verbose_name=_("model"),
        related_name='cars',
    )
    avg_rating = models.DecimalField(
        _('average rating'),
        default=1,
        decimal_places=1,
        max_digits=2,
    )

    def __str__(self):
        return f"{self.make} - {self.model}"

    class Meta:
        verbose_name = _("Car")
        verbose_name_plural = _("Cars")

    def update_rating(self):
        self.avg_rating = self.calculate_avg_rating()
        self.save()

    def calculate_avg_rating(self):
        """ Calculate average rating """
        result = self.reviews.all().aggregate(
            sum=models.Sum('rating'),
            count=models.Count('id'),
        )
        reviews_sum = result.get('sum', 0)
        reviews_count = result.get('count', 0)
        rating = 0
        if reviews_count > 0:
            rating = float(reviews_sum) / reviews_count
        return rating

    @cached_property
    def rates_number(self):
        return self.reviews.count()
