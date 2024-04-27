# Generated by Django 5.0.3 on 2024-04-26 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("calls", "0004_alter_operator_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="operator",
            name="subscribers",
            field=models.ManyToManyField(
                blank=True,
                through="calls.OperatorSubscriber",
                to="calls.subscriber",
                verbose_name="subscribers",
            ),
        ),
        migrations.AlterField(
            model_name="subscriber",
            name="operators",
            field=models.ManyToManyField(
                blank=True,
                through="calls.OperatorSubscriber",
                to="calls.operator",
                verbose_name="operators",
            ),
        ),
    ]