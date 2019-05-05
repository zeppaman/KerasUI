from django.conf.urls import url, include
from rest_framework import routers
from api import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'datasetitem', views.DataSetItemViewSet)
router.register(r'dataset', views.DataSetViewSet)
router.register(r'test', views.TestItemViewSet, basename='test')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

urlpatterns += staticfiles_urlpatterns()
