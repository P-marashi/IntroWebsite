from django.urls import path, include

from . import apis


urlpatterns = [
     path('', apis.ListCreateProjectAPIView.as_view(),
          name="project_create_list"),
     path('<int:project_pk>/', include([
          path('', apis.RetrieveUpdateDestroyProjectAPIView.as_view(),
               name="project_retrive_update_destroy"),
          path('<int:project_pk>/features/', include([
               path('', apis.ListCreateProjectFeatureAPIView.as_view(),
                    name="create_list_features"),
               path('<int:feature_pk>/',
                    apis.UpdateDestroyProjectFeatureAPIView.as_view(),
                    name="feature_update_destroy"),
               ])),
          path('<int:project_pk>/images/', include([
               path('', apis.ListCreateProjectImageExampleAPIView.as_view(),
                    name="create_list_image"),
               path('<int:image_pk>/',
                    apis.UpdateDestroyProjectImageExampleAPIView.as_view(),
                    name="image_update_destroy")
               ]))
          ]))
]
