# Generated by Django 5.0.2 on 2024-02-28 14:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0002_course_duration_course_instructor_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="course_image",
            field=models.ImageField(null=True, upload_to="course_images/"),
        ),
    ]
