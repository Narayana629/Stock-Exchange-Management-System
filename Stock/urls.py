from django.conf.urls.static import static
from django.urls import path
from . import views
from SES import settings

urlpatterns = [

    path('',views.overview,name="overview"),
    path('activity', views.activity, name="activity"),
path('profile', views.profile, name="profile"),
    path('wallet', views.wallet, name="wallet"),
    path('buystocks', views.buystocks, name="buystocks"),
    path('sellstocks', views.sellstocks, name="sellstocks"),
path('viewstock', views.viewstock, name="viewstock"),
path('logout', views.logout, name="logout"),
path('api', views.ChartData.as_view()),


]
