# Generated by Django 5.0.6 on 2024-07-24 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Computer_Science_and_Engineering',
            fields=[
                ('student_ID', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50)),
                ('password', models.CharField(max_length=200)),
                ('phone', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('course_ID', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('course_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Fees_details',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('course_id', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=50)),
                ('amount', models.IntegerField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('status', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Information_Science_and_Engineering',
            fields=[
                ('student_ID', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50)),
                ('password', models.CharField(max_length=200)),
                ('phone', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='login',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50)),
                ('email', models.EmailField(max_length=50)),
                ('password', models.CharField(max_length=200)),
                ('phone', models.BigIntegerField(blank=True, default=0)),
            ],
        ),
    ]
