# Generated by Django 4.2.15 on 2024-08-31 12:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Allocation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("exam_name", models.CharField()),
                ("exam_center_id", models.IntegerField()),
                ("roll_number", models.CharField()),
                ("exam_date", models.DateField()),
                ("exam_time", models.CharField()),
            ],
        ),
        migrations.CreateModel(
            name="Exam",
            fields=[
                ("exam_id", models.IntegerField(primary_key=True, serialize=False)),
                ("exam_name", models.CharField(max_length=100)),
                ("exam_date", models.DateField()),
                ("instruction", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="ExamCenter",
            fields=[
                (
                    "exam_center_id",
                    models.IntegerField(primary_key=True, serialize=False),
                ),
                ("center_name", models.CharField(max_length=100)),
                ("total_capacity", models.IntegerField()),
                (
                    "exam_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="exam_allocation.exam",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Student",
            fields=[
                (
                    "student_id",
                    models.BigIntegerField(primary_key=True, serialize=False),
                ),
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                (
                    "roll_number",
                    models.CharField(blank=True, max_length=1000, null=True),
                ),
                ("aadhar_number", models.CharField(max_length=12)),
                ("date_of_birth", models.DateField()),
                (
                    "exam_center_choice",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="exam_allocation.examcenter",
                    ),
                ),
                (
                    "exam_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="exam_allocation.exam",
                    ),
                ),
            ],
        ),
    ]