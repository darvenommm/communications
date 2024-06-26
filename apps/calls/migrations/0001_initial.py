# Generated by Django 5.0.6 on 2024-05-28 21:25

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import library.models.mixins.created_mixin.main
import library.models.mixins.updated_mixin.main
import library.models.validators.duration_positivity_validator.main
import library.models.validators.time_range_validator.main


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunSQL("create schema if not exists communications;"),
        migrations.CreateModel(
            name="Operator",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        blank=True,
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        db_index=True, max_length=100, unique=True, verbose_name="title"
                    ),
                ),
                (
                    "foundation_date",
                    models.DateField(
                        validators=[
                            library.models.validators.time_range_validator.main.TimeRangeValidator()
                        ],
                        verbose_name="foundation date",
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        blank=True, default="", max_length=2500, verbose_name="description"
                    ),
                ),
            ],
            options={
                "verbose_name": "operator",
                "verbose_name_plural": "operators",
                "db_table": '"communications"."operator"',
                "ordering": ("title", "foundation_date"),
            },
            bases=(
                library.models.mixins.created_mixin.main.CreatedMixin,
                library.models.mixins.updated_mixin.main.UpdatedMixin,
                models.Model,
            ),
        ),
        migrations.CreateModel(
            name="OperatorSubscriber",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        blank=True,
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "operator",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="calls.operator",
                        verbose_name="operator",
                    ),
                ),
                (
                    "subscriber",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="subscriber",
                    ),
                ),
            ],
            options={
                "verbose_name": "relation of operator and subscriber",
                "verbose_name_plural": "relations of operator and subscriber",
                "db_table": '"communications"."operator_subscriber"',
                "unique_together": {("operator", "subscriber")},
            },
        ),
        migrations.AddField(
            model_name="operator",
            name="subscribers",
            field=models.ManyToManyField(
                blank=True,
                through="calls.OperatorSubscriber",
                to=settings.AUTH_USER_MODEL,
                verbose_name="subscribers",
            ),
        ),
        migrations.CreateModel(
            name="SubscriberCall",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        blank=True,
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "start",
                    models.DateTimeField(
                        validators=[
                            library.models.validators.time_range_validator.main.TimeRangeValidator()
                        ],
                        verbose_name="start time",
                    ),
                ),
                (
                    "duration",
                    models.DurationField(
                        validators=[
                            library.models.validators.duration_positivity_validator.main.duration_positivity_validator
                        ],
                        verbose_name="duration",
                    ),
                ),
                (
                    "caller",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="made_calls",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="caller",
                    ),
                ),
                (
                    "receiver",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="received_calls",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="call receiver",
                    ),
                ),
            ],
            options={
                "verbose_name": "subscriber call",
                "verbose_name_plural": "subscribers calls",
                "db_table": '"communications"."subscriber_call"',
                "ordering": (
                    "caller__first_name",
                    "caller__last_name",
                    "receiver__first_name",
                    "receiver__last_name",
                ),
            },
            bases=(
                library.models.mixins.created_mixin.main.CreatedMixin,
                library.models.mixins.updated_mixin.main.UpdatedMixin,
                models.Model,
            ),
        ),
        migrations.AddConstraint(
            model_name="subscribercall",
            constraint=models.CheckConstraint(
                check=models.Q(("caller_id", models.F("receiver_id")), _negated=True),
                name="check_not_equal_caller_and_receiver",
            ),
        ),
    ]
