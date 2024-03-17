from django import template

from ..models import Clan, Player, PlayerPromotion, ClanBattle, BattleDetail

register = template.Library()


@register.simple_tag
def get_player(p_id):
    player = Player.objects.get(player_id=p_id)
    return player


@register.simple_tag
def player_tier(player, upper):
    tier_dic = {'B': 'bronze', 'S': 'silver', 'G': 'gold', 'D': 'diamond', 'L': 'legend'}
    tier = tier_dic[player.tier]
    if upper:
        return tier.upper()
    else:
        return tier


@register.simple_tag
def player_rank(player):
    players = Player.objects.filter(tier=player.tier).order_by('tier_rank', '-point')
    for i in range(len(players)):
        if player == players[i]:
            return i + 1
    return -1


@register.simple_tag
def get_p_promo(p_id):
    promo = PlayerPromotion.objects.get(player_id=p_id)
    return promo


# BATTLE
@register.simple_tag
def get_p_point(is_winner, b_no):
    battle = ClanBattle.objects.get(battle_no=b_no)
    if is_winner:
        return '+ ' + str(battle.point)
    return '- ' + str(battle.point)


@register.simple_tag
def get_p_oppo_clan(is_winner, b_no):
    battle = ClanBattle.objects.get(battle_no=b_no)
    if is_winner:
        return Clan.objects.get(clan_id=battle.loser)
    else:
        return Clan.objects.get(clan_id=battle.winner)