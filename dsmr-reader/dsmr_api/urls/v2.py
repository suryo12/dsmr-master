from django.conf.urls import url, include

from dsmr_api.views import v2 as views


datalogger_url_patterns = [
    url(r'^dsmrreading$', views.DsmrReadingViewSet.as_view({
        'get': 'list',
        'post': 'create',
    }), name='dsmrreading'),
]

consumption_url_patterns = [
    url(r'^electricity$', views.ElectricityConsumptionViewSet.as_view({
        'get': 'list',
    }), name='electricity-consumption'),
    url(r'^gas$', views.GasConsumptionViewSet.as_view({
        'get': 'list',
    }), name='gas-consumption'),
]

statistics_url_patterns = [
    url(r'^day$', views.DayStatisticsViewSet.as_view({
        'get': 'list',
    }), name='day-statistics'),
    url(r'^hour$', views.HourStatisticsViewSet.as_view({
        'get': 'list',
    }), name='hour-statistics'),
]

urlpatterns = [
    url(r'^datalogger/', include(datalogger_url_patterns)),
    url(r'^consumption/', include(consumption_url_patterns)),
    url(r'^statistics/', include(statistics_url_patterns)),
]
