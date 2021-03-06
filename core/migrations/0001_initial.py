# Generated by Django 3.2.7 on 2021-09-30 16:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avg_rating', models.DecimalField(decimal_places=1, default=1, max_digits=2, verbose_name='average rating')),
            ],
            options={
                'verbose_name': 'Car',
                'verbose_name_plural': 'Cars',
            },
        ),
        migrations.CreateModel(
            name='Make',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
            ],
            options={
                'verbose_name': 'Make',
                'verbose_name_plural': 'Makes',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(choices=[(1, 'Very Bad'), (2, 'Bad'), (3, 'Poor'), (4, 'Good'), (5, 'Excellent')], verbose_name='rating')),
                ('review_datetime', models.DateTimeField(auto_now_add=True, verbose_name='review add datetime')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='core.car', verbose_name='car')),
            ],
            options={
                'verbose_name': 'Review',
                'verbose_name_plural': 'Reviews',
                'ordering': ('-review_datetime',),
            },
        ),
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('make', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='models', to='core.make', verbose_name='make')),
            ],
            options={
                'verbose_name': 'Model',
                'verbose_name_plural': 'Models',
                'ordering': ('title',),
            },
        ),
        migrations.AddField(
            model_name='car',
            name='make',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cars', to='core.make', verbose_name='make'),
        ),
        migrations.AddField(
            model_name='car',
            name='model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cars', to='core.model', verbose_name='model'),
        ),
    ]
