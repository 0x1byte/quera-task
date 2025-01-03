# Generated by Django 5.1.4 on 2024-12-15 14:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Form',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='عنوان')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='ایجاد شده در')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='متن سوال')),
                ('question_type', models.CharField(choices=[('short_text', 'متن کوتاه پاسخ'), ('long_text', 'متن بلند پاسخ'), ('email', 'ایمیل'), ('numeric', 'پاسخ عددی')], max_length=20, verbose_name='نوع سوال')),
                ('required', models.BooleanField(default=False, verbose_name='اجباری است؟')),
                ('min_value', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='کمترین مقدار (برای سوال عددی)')),
                ('max_value', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='بیشترین مقدار (برای سوال عددی)')),
                ('max_length', models.PositiveIntegerField(blank=True, null=True, verbose_name='حداکثر طول (برای متن)')),
                ('allow_decimal', models.BooleanField(default=True, verbose_name='مجاز به اعشار (برای عددی)')),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='form.form')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response_text', models.TextField(blank=True, null=True, verbose_name='متن پاسخ')),
                ('response_number', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='پاسخ عددی')),
                ('response_email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='پاسخ ایمیل')),
                ('submitted_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ارسال پاسخ')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='form.question', verbose_name='سوال')),
            ],
        ),
    ]
