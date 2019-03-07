# Generated by Django 2.1.7 on 2019-03-07 14:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Hierarchy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eat_better.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Nutriments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fats', models.DecimalField(decimal_places=1, max_digits=3)),
                ('sugars', models.DecimalField(decimal_places=1, max_digits=3)),
                ('saturated_fat', models.DecimalField(decimal_places=1, max_digits=3)),
                ('salt', models.DecimalField(decimal_places=3, max_digits=4)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('nutriscore', models.CharField(max_length=1)),
                ('url', models.CharField(max_length=255)),
                ('category', models.ManyToManyField(through='eat_better.Hierarchy', to='eat_better.Category')),
                ('nutriments', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='eat_better.Nutriments')),
            ],
        ),
        migrations.AddField(
            model_name='hierarchy',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eat_better.Product'),
        ),
    ]
