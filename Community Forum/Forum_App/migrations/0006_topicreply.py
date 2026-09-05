from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('Forum_App', '0005_topic_info_system_name_topic_info_username_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TopicReply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='', max_length=255)),
                ('body', models.TextField(max_length=5000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='Forum_App.topic_info')),
            ],
            options={
                'ordering': ('created_at', 'id'),
            },
        ),
    ]
