# Generated by Django 4.0 on 2021-12-24 21:08

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_phone', models.CharField(blank=True, max_length=200, null=True, unique=True)),
                ('user_other', models.CharField(blank=True, max_length=200, null=True)),
                ('user_profile_image', models.ImageField(blank=True, default='profiles/default-image.jpg', null=True, upload_to='profiles')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Donation_Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000, null=True)),
                ('goal', models.PositiveIntegerField(null=True)),
                ('amount_received', models.PositiveIntegerField(blank=True, default=0)),
                ('description', models.TextField(null=True)),
                ('updates', models.TextField(blank=True, default='')),
                ('status', models.CharField(default='active', max_length=10)),
                ('short_description', models.CharField(blank=True, max_length=50, null=True)),
                ('request_image', models.ImageField(default='donations/default-image.jpg', null=True, upload_to='donations')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.user')),
            ],
        ),
        migrations.CreateModel(
            name='Donation_made',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(null=True)),
                ('note', models.CharField(blank=True, max_length=200, null=True)),
                ('status', models.CharField(default='Incomplete', max_length=10)),
                ('donation_id', models.CharField(blank=True, default=None, max_length=100, null=True, unique=True)),
                ('datetime_of_payment', models.DateTimeField(default=django.utils.timezone.now)),
                ('razorpay_order_id', models.CharField(blank=True, max_length=500, null=True)),
                ('razorpay_payment_id', models.CharField(blank=True, max_length=500, null=True)),
                ('razorpay_signature', models.CharField(blank=True, max_length=500, null=True)),
                ('donation_request', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='donation_request', to='accounts.donation_request')),
                ('from_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='donation_from_user', to='accounts.user')),
                ('to_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='donation_to_user', to='accounts.user')),
            ],
        ),
    ]
