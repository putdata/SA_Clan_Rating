# Generated by Django 2.1.4 on 2019-02-05 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BattleDetail',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('battle_no', models.CharField(max_length=16)),
                ('player_id', models.CharField(max_length=13)),
                ('is_winner', models.BooleanField(default=False)),
                ('kill', models.PositiveSmallIntegerField(default=0)),
                ('death', models.PositiveSmallIntegerField(default=0)),
                ('point', models.SmallIntegerField(default=0)),
                ('is_mom', models.BooleanField(default=False)),
                ('is_promo', models.BooleanField(default=False)),
                ('rejoin', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'battle_detail',
            },
        ),
        migrations.CreateModel(
            name='Clan',
            fields=[
                ('clan_id', models.CharField(max_length=12, primary_key=True, serialize=False)),
                ('clan_home', models.CharField(max_length=16)),
                ('clan_name', models.CharField(max_length=20)),
                ('mark_f', models.CharField(max_length=16)),
                ('mark_b', models.CharField(max_length=16)),
                ('rating', models.SmallIntegerField(default=1000)),
                ('limit_r', models.PositiveSmallIntegerField(default=0)),
                ('win', models.PositiveSmallIntegerField(default=0)),
                ('lose', models.PositiveSmallIntegerField(default=0)),
                ('l_win', models.PositiveSmallIntegerField(default=0)),
                ('l_lose', models.PositiveSmallIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('caution', models.SmallIntegerField(default=0)),
                ('visibility', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'clan',
            },
        ),
        migrations.CreateModel(
            name='ClanBattle',
            fields=[
                ('battle_no', models.CharField(max_length=16, primary_key=True, serialize=False)),
                ('winner', models.CharField(max_length=12)),
                ('loser', models.CharField(max_length=12)),
                ('point', models.PositiveSmallIntegerField(default=0)),
                ('battled_at', models.DateTimeField()),
            ],
            options={
                'db_table': 'battle',
            },
        ),
        migrations.CreateModel(
            name='ClanComment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('clan_id', models.CharField(max_length=12)),
                ('user_id', models.CharField(max_length=50)),
                ('text', models.CharField(default='내용 없음.', max_length=30)),
                ('anonymous', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'clan_comment',
            },
        ),
        migrations.CreateModel(
            name='DidBattle',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('clan_id', models.CharField(max_length=12)),
                ('battle_no', models.CharField(max_length=16)),
            ],
            options={
                'db_table': 'did_battle',
            },
        ),
        migrations.CreateModel(
            name='EmailAuth',
            fields=[
                ('user_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=10)),
                ('token', models.CharField(max_length=32)),
            ],
            options={
                'db_table': 'web_user_auth',
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('player_id', models.CharField(max_length=13, primary_key=True, serialize=False)),
                ('clan_id', models.CharField(max_length=12, null=True)),
                ('name', models.CharField(max_length=20)),
                ('tier', models.CharField(default='B', max_length=1)),
                ('tier_rank', models.PositiveSmallIntegerField(default=3)),
                ('point', models.SmallIntegerField(default=0)),
                ('promo', models.BooleanField(default=False)),
                ('win', models.PositiveSmallIntegerField(default=0)),
                ('lose', models.PositiveSmallIntegerField(default=0)),
                ('l_win', models.PositiveSmallIntegerField(default=0)),
                ('l_lose', models.PositiveSmallIntegerField(default=0)),
                ('kill', models.PositiveIntegerField(default=0)),
                ('death', models.PositiveIntegerField(default=0)),
                ('l_kill', models.PositiveIntegerField(default=0)),
                ('l_death', models.PositiveIntegerField(default=0)),
                ('mom', models.PositiveSmallIntegerField(default=0)),
                ('report', models.PositiveSmallIntegerField(default=0)),
                ('msg', models.CharField(max_length=50, null=True)),
                ('visibility', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'player',
            },
        ),
        migrations.CreateModel(
            name='PlayerComment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('player_id', models.CharField(max_length=13)),
                ('user_id', models.CharField(max_length=50)),
                ('text', models.CharField(default='내용 없음.', max_length=30)),
                ('anonymous', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'player_comment',
            },
        ),
        migrations.CreateModel(
            name='PlayerPromotion',
            fields=[
                ('player_id', models.CharField(max_length=13, primary_key=True, serialize=False)),
                ('win', models.PositiveSmallIntegerField(default=0)),
                ('lose', models.PositiveSmallIntegerField(default=0)),
            ],
            options={
                'db_table': 'player_promo',
            },
        ),
        migrations.CreateModel(
            name='WebUser',
            fields=[
                ('user_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=100)),
                ('player_id', models.CharField(max_length=13, null=True, unique=True)),
                ('name', models.CharField(max_length=10)),
                ('cash', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('admin', models.PositiveSmallIntegerField(default=0)),
            ],
            options={
                'db_table': 'web_user',
            },
        ),
    ]
