from argparse import Action
from ast import Delete
from asyncio import exceptions
from distutils.log import error
from email import message
import json
from urllib import request
from django.http import Http404,JsonResponse
from django.shortcuts import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import Comment, Issue, Project , Contributor
from rest_framework import viewsets , permissions , generics
from API.serializer import ProjectSerializer, ContributorSerializer , IssueSerializer , CommentSerializer, UserProjectSerializer ,UserSerializer
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
# Create your views here.



class UserViewSet(ModelViewSet):
    """
    Point de terminaison API qui permet aux User d'être affichés ou modifiés.
    """
    serializer_class = UserProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):

        
        return Project.objects.all()


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ProjectViewSet(ModelViewSet):
    """
    Point de terminaison API qui permet aux projet d'être affichés ou modifiés.
    """
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        
        
    

        return Project.objects.all()

class ContributorViewSet(ModelViewSet):
    """
    Point de terminaison API qui permet aux users (contributor) d'être affichés ou modifiés.
    """
    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        
        if self.request.method == 'GET':
            try:   
                return Contributor.objects.filter(project_id=self.kwargs['projects_pk'])
            except Contributor.DoesNotExist:
                return JsonResponse({}, safe=False, status=status.HTTP_201_CREATED)



    def get_permissions(self):

        id = self.request.user.id
   
        if self.action in ["delete","update","destroy"] :
            contributor = get_object_or_404(Contributor, pk=self.kwargs["pk"])

      
            if id != contributor.user_id.id :
                raise PermissionDenied()
        return super().get_permissions()
        
    def delete(self,project_id,users_id):

            try:
                contributor = Contributor.objects.get(pk=users_id) 
                contributor.delete()
            except Contributor.DoesNotExist:
                return JsonResponse({"error":"L'id du Contributeur n'a pas été trouvé ou a déjà été supprimer !!"}, safe=False, status=status.HTTP_404_NOT_FOUND)
            return HttpResponse(status=status.HTTP_204_NO_CONTENT)
     
     


class IssueViewSet(ModelViewSet):
    """
    Point de terminaison API qui permet aux Issue d'être affichés ou modifiés.
    """
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        
        print(self.kwargs)
        return Issue.objects.filter(project_id=self.kwargs['projects_pk'])

    def get_permissions(self):
        id = self.request.user.id
        if self.action in ["delete","update","destroy"] :
            issue = get_object_or_404(Issue, pk=self.kwargs["pk"])
            if id != issue.author_user_id.id :
                raise PermissionDenied()
            
        return super().get_permissions()


class CommentViewSet(ModelViewSet):
    """
    Point de terminaison API qui permet aux comment d'être affichés ou modifiés.
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):

        print(self.kwargs)

    
        project = get_object_or_404(Project,pk=self.kwargs["projects_pk"])
        issue = Issue.objects.filter(pk=self.kwargs['project_issue_pk']).first()

        if issue and project.pk == issue.project_id.pk :
            
            return Comment.objects.filter(issue_id=self.kwargs['project_issue_pk'])

        else:

            raise Http404("Issue pas trouvé dans le projet")
        
            

    def get_permissions(self):
        id = self.request.user.id
        print(id)

        if self.action in ["delete","update","destroy"] :
           
            comment = get_object_or_404(Comment, pk=self.kwargs["pk"])

            if id != comment.author_user_id.id :
                raise PermissionDenied()

        return super().get_permissions()
