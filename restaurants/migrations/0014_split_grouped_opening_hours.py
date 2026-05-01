from django.db import migrations


WEEKDAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
WEEKENDS = ['saturday', 'sunday']


def split_grouped_days(apps, schema_editor):
    OpeningHours = apps.get_model('restaurants', 'OpeningHours')
    for row in list(OpeningHours.objects.filter(day__in=['weekdays', 'weekends'])):
        target_days = WEEKDAYS if row.day == 'weekdays' else WEEKENDS
        for day in target_days:
            OpeningHours.objects.get_or_create(
                restaurant=row.restaurant,
                day=day,
                defaults={
                    'open_time': row.open_time,
                    'close_time': row.close_time,
                },
            )
        row.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0013_alter_openinghours_day'),
    ]

    operations = [
        migrations.RunPython(split_grouped_days, reverse_code=migrations.RunPython.noop),
    ]
