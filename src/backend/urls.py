from django.contrib import admin
    


from .apps.main import views as mainViews
from .apps.clan import views as clanViews
from .apps.player import views as playerViews
from .apps.battle import views as battleViews
from .apps.board import views as boardViews
from django_summernote.views import SummernoteEditor, SummernoteUploadAttachment

urlpatterns = [
    path('test', clanViews.test2),
    path('', mainViews.index),
    path('signin', mainViews.signin),
    path('signout', mainViews.signout),
    path('signup', mainViews.signup),
    path('clan', clanViews.clan),
    path('clan/regist', clanViews.clan_regist),
    path('search/<word>', mainViews.search),
    re_path(r'^clan/(?P<c_id>[0-9]{12})$', clanViews.clan_detail),
    re_path(r'^clan/(?P<tier>[a-zA-Z]*)$', clanViews.clan_list),
    re_path(r'^battle/(?P<b_no>[0-9]{16})$', battleViews.battle_detail),
    re_path(r'^player/(?P<p_id>[0-9]{1,13})$', playerViews.player_detail),
    re_path(r'^battle/c/(?P<c_id>[0-9]{12})/(?P<count>[0-9]*)$', battleViews.battle_c_more),
    re_path(r'^battle/p/(?P<p_id>[0-9]{1,13})/(?P<count>[0-9]*)$', battleViews.battle_p_more),
    # 방명록
    re_path(r'^clan/(?P<c_id>[0-9]{12})/new_c$', clanViews.new_comment),
    re_path(r'^clan/(?P<c_id>[0-9]{12})/get_c/(?P<count>[0-9]*)$', clanViews.get_comment),
    re_path(r'^player/(?P<p_id>[0-9]{1,13})/new_c$', playerViews.new_comment),
    re_path(r'^player/(?P<p_id>[0-9]{1,13})/get_c/(?P<count>[0-9]*)$', playerViews.get_comment),


    # 보드

    # 인증토큰
    path('regist/activate', mainViews.regist_activate),


    # 약관들
    path('service/tos', mainViews.tos),
    path('service/policy', mainViews.policy)
]
