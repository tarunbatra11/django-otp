from oauth2_provider import views
from django.conf.urls import include, url
from django.contrib import admin

from otp.extended.mixins import ExtendedTokenView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^otp/', include('otp.urls'), name='otp'),
    url(r'^api/v1/', include('api.urls'), name='api'),
]

# oauth2_provider urls
urlpatterns += (
        url(r'^o/authorize/$', views.AuthorizationView.as_view(), name="authorize"),
        url(r'^o/token/$', views.TokenView.as_view(), name="token"),
        url(r'^o/extended_token/$', ExtendedTokenView.as_view(), name="token"),
        url(r'^o/revoke_token/$', views.RevokeTokenView.as_view(), name="revoke-token"),
)
# Application management views
urlpatterns += (
        url(r'^o/applications/$', views.ApplicationList.as_view(), name="list"),
        url(r'^o/applications/register/$', views.ApplicationRegistration.as_view(), name="register"),
        url(r'^o/applications/(?P<pk>\d+)/$', views.ApplicationDetail.as_view(), name="detail"),
        url(r'^o/applications/(?P<pk>\d+)/delete/$', views.ApplicationDelete.as_view(), name="delete"),
        url(r'^o/applications/(?P<pk>\d+)/update/$', views.ApplicationUpdate.as_view(), name="update"),
)
urlpatterns += (
        url(r'^o/authorized_tokens/$', views.AuthorizedTokensListView.as_view(), name="authorized-token-list"),
        url(r'^o/authorized_tokens/(?P<pk>\d+)/delete/$', views.AuthorizedTokenDeleteView.as_view(),
                    name="authorized-token-delete"),
)
# required for reversing namespace, above urls will override this
urlpatterns += (
        url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
)
