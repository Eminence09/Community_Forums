from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ('Forum_App', '0006_topicreply'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic_info',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]