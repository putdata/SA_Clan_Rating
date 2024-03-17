from django.db import models


# WEBSITE USER
class WebUser(models.Model):  # 웹사이트 유저
    user_id = models.CharField(max_length=50, primary_key=True)
    password = models.CharField(max_length=100)
    player_id = models.CharField(max_length=13, null=True, unique=True)
    name = models.CharField(max_length=10)
    cash = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    admin = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = 'web_user'


class EmailAuth(models.Model):  # 인증키
    user_id = models.CharField(max_length=50, primary_key=True)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=10)
    token = models.CharField(max_length=32)

    class Meta:
        db_table = 'web_user_auth'


# CLAN MODELS
class Clan(models.Model):  # 클랜
    clan_id = models.CharField(max_length=12, primary_key=True)
    clan_home = models.CharField(max_length=16)
    clan_name = models.CharField(max_length=20)
    mark_f = models.CharField(max_length=16)
    mark_b = models.CharField(max_length=16)
    rating = models.SmallIntegerField(default=1000)
    limit_r = models.PositiveSmallIntegerField(default=0)
    win = models.PositiveSmallIntegerField(default=0)
    lose = models.PositiveSmallIntegerField(default=0)
    l_win = models.PositiveSmallIntegerField(default=0)
    l_lose = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    caution = models.SmallIntegerField(default=0)
    visibility = models.BooleanField(default=True)

    class Meta:
        db_table = 'clan'


# PLAYER MODEL
class Player(models.Model):  # 플레이어
    player_id = models.CharField(max_length=13, primary_key=True)
    clan_id = models.CharField(max_length=12, null=True)
    name = models.CharField(max_length=20)
    tier = models.CharField(max_length=1, default='B')
    tier_rank = models.PositiveSmallIntegerField(default=3)
    point = models.SmallIntegerField(default=0)
    promo = models.BooleanField(default=False)
    win = models.PositiveSmallIntegerField(default=0)
    lose = models.PositiveSmallIntegerField(default=0)
    l_win = models.PositiveSmallIntegerField(default=0)
    l_lose = models.PositiveSmallIntegerField(default=0)
    kill = models.PositiveIntegerField(default=0)
    death = models.PositiveIntegerField(default=0)
    l_kill = models.PositiveIntegerField(default=0)
    l_death = models.PositiveIntegerField(default=0)
    mom = models.PositiveSmallIntegerField(default=0)
    report = models.PositiveSmallIntegerField(default=0)
    msg = models.CharField(max_length=50, null=True)
    visibility = models.BooleanField(default=True)

    class Meta:
        db_table = 'player'


class PlayerPromotion(models.Model):  # 플레이어 승급전 정보
    player_id = models.CharField(max_length=13, primary_key=True)
    win = models.PositiveSmallIntegerField(default=0)
    lose = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = 'player_promo'


# RECORD MODEL
class ClanBattle(models.Model):  # 클랜전 기록
    battle_no = models.CharField(max_length=16, primary_key=True)
    winner = models.CharField(max_length=12)
    loser = models.CharField(max_length=12)
    point = models.PositiveSmallIntegerField(default=0)
    battled_at = models.DateTimeField()

    class Meta:
        db_table = 'battle'


class DidBattle(models.Model):
    id = models.AutoField(primary_key=True)
    clan_id = models.CharField(max_length=12)
    battle_no = models.CharField(max_length=16)

    class Meta:
        db_table = 'did_battle'


class BattleDetail(models.Model):  # 클랜전 상세 기록 (유저 데이터)
    id = models.AutoField(primary_key=True)
    battle_no = models.CharField(max_length=16)
    player_id = models.CharField(max_length=13)
    is_winner = models.BooleanField(default=False)
    kill = models.PositiveSmallIntegerField(default=0)
    death = models.PositiveSmallIntegerField(default=0)
    point = models.SmallIntegerField(default=0)
    is_mom = models.BooleanField(default=False)
    is_promo = models.BooleanField(default=False)
    rejoin = models.BooleanField(default=False)

    class Meta:
        db_table = 'battle_detail'


# 방명록
class ClanComment(models.Model):
    id = models.AutoField(primary_key=True)
    clan_id = models.CharField(max_length=12)
    user_id = models.CharField(max_length=50)
    text = models.CharField(max_length=30, default='내용 없음.')
    anonymous = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'clan_comment'


class PlayerComment(models.Model):
    id = models.AutoField(primary_key=True)
    player_id = models.CharField(max_length=13)
    user_id = models.CharField(max_length=50)
    text = models.CharField(max_length=30, default='내용 없음.')
    anonymous = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'player_comment'


# 서머노트
from django_summernote import models as summer_model
from django_summernote import fields as summer_fields


class SummerNote(summer_model.Attachment):
    summer_field = summer_fields.SummernoteTextField(default='')