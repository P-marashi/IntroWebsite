from django.urls import path, include

from . import apis


urlpatterns = [
    path('create/', apis.CreateProjectAPIView.as_view(),
         name="create_project"),
    path('update/<int:pk>/', apis.UpdateProjectAPIView.as_view(),
         name="update_project"),
    path('delete/<int:pk>/', apis.DestroyProjectAPIView.as_view(),
         name="destroy_project"),
    path('list/', apis.ListProjectAPIView.as_view(),
         name="list_project"),

    path('<int:pk>/', include([
        path('', apis.RetrieveProjectAPIView.as_view(),
             name="retreive_project"),
        path('feature/', include([
            path('create/', apis.CreateProjectFeatureAPIView.as_view(),
                 name="create_project_feature"),
            path('update/<int:pk>/', apis.UpdateProjectFeatureAPIView.as_view(),
                 name="update_project_feature"),
            path('delete/<int:pk>/', apis.DestroyProjectFeatureAPIView.as_view(),
                 name="destroy_project_feature"),
            path('list/', apis.ListProjectFeatureAPIView.as_view(),
                 name="list_project_feature"),
        ])),
        path('image/', include([
            path('create/', apis.CreateProjectImageExampleAPIView.as_view(),
                 name="create_project_image"),
            path('update/<int:pk>/', apis.UpdateProjectImageExampleAPIView.as_view(),
                 name="update_project_image"),
            path('delete/<int:pk>/', apis.DestroyProjectImageExampleAPIView.as_view(),
                 name="destroy_project_image"),
            path('list/', apis.ListProjectImageExampleAPIView.as_view(),
                 name="list_project_image"),
        ])),
    ])),
]
