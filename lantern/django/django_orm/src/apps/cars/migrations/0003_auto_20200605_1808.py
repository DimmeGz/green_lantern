# Generated by Django 3.0.6 on 2020-06-05 18:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dealers', '0002_auto_20200605_1808'),
        ('cars', '0002_populate_colors'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarEngine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
            ],
            options={
                'verbose_name': 'Engine Type',
                'verbose_name_plural': 'Engine Types',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='FuelType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=12, unique=True)),
            ],
            options={
                'verbose_name': 'Fuel Type',
                'verbose_name_plural': 'Fuel Types',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='car',
            name='color',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cars.Color'),
        ),
        migrations.AddField(
            model_name='car',
            name='dealer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cars', to='dealers.Dealer'),
        ),
        migrations.AddField(
            model_name='car',
            name='doors',
            field=models.PositiveSmallIntegerField(default=4),
        ),
        migrations.AddField(
            model_name='car',
            name='engine_power',
            field=models.DecimalField(decimal_places=2, max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='car',
            name='first_registration_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='car',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='car',
            name='sitting_places',
            field=models.PositiveSmallIntegerField(default=4),
        ),
        migrations.CreateModel(
            name='CarProperty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='cars.Car')),
                ('property', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='cars.Property')),
            ],
        ),
        migrations.AddIndex(
            model_name='carengine',
            index=models.Index(fields=['name'], name='cars_careng_name_1f7da2_idx'),
        ),
        migrations.AddField(
            model_name='car',
            name='engine_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cars.CarEngine'),
        ),
        migrations.AddField(
            model_name='car',
            name='fuel_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cars.FuelType'),
        ),
    ]
