# Generated by Django 5.0.1 on 2024-01-26 08:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('times_used', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='RecipeProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.IntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cook_book.product')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cook_book.recipe')),
            ],
            options={
                'unique_together': {('recipe', 'product')},
            },
        ),
        migrations.AddField(
            model_name='recipe',
            name='products',
            field=models.ManyToManyField(related_name='recipes', through='cook_book.RecipeProduct', to='cook_book.product'),
        ),
    ]
