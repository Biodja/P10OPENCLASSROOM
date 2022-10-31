"""softdesk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from pathlib import Path
from django.contrib import admin
from django.urls import include, path
from django.views import View
from rest_framework_nested import routers
from API.views import ContributorViewSet , ProjectViewSet , IssueViewSet , CommentViewSet, UserCreate , UserViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')

project_router = routers.NestedSimpleRouter(router, r'projects', lookup='projects')
project_router.register(r'issues', IssueViewSet, basename='project_issue')

issue_router = routers.NestedSimpleRouter(project_router, r'issues', lookup='project_issue')
issue_router.register(r'comments', CommentViewSet, basename='project_issue_comment')


contributor_router = routers.NestedSimpleRouter(router, r'projects', lookup='projects')
contributor_router.register(r'users', ContributorViewSet, basename='contributor_project')



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', include(project_router.urls)),
    path('api/', include(issue_router.urls)),
    path('api/', include(contributor_router.urls)),
    path('api/logins/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/signup/', UserCreate.as_view(), name='signup'),

    path('api/projects/<int:project_id>/users/<int:users_id>',ContributorViewSet.delete , name="associate_project"),


]
