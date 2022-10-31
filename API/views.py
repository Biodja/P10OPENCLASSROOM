from argparse import Action
from ast import Delete
from asyncio import exceptions
from distutils.log import error
from email import message
import json
from urllib import request
from django.http import Http404,JsonResponse
from django.shortcuts import HttpResponse, render
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import Comment, Issue, Project , Contributor
from rest_framework import viewsets , permissions , generics
from API.serializer import ProjectSerializer, ContributorSerializer , IssueSerializer , CommentSerializer, UserProjectSerializer ,UserSerializer
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth import get_user_model
# Create your views here.



class UserViewSet(ModelViewSet):
    """
    Point de terminaison API qui permet aux User d'être affichés ou modifiés.
    """
    serializer_class = UserProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):

        
        return Project.objects.all()
    
"""
@api_view(['POST', 'GET'])
def associate_user_project (request,project_id,user=None):
    

    print("requette:",request.data)
    user_id = request.data.get("user_id")
    print(project_id)
    print("id :",user_id)

    if request.method == 'POST':
        try:

            project = Project.objects.get(pk=project_id)

                 
            print("project_id :",project.id)
            print("user_id :",user_id)
                
            user = User.objects.get(pk=user_id)

            print("user:",project.author_user_id.id)

            print("c'est la avant :",project.project_members.all())
            project.project_members.add(user_id)
            project.save()
            print("c'est la apres :",project.project_members.all())

        except Project.DoesNotExist:
            return JsonResponse({}, safe=False, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'GET':
        try:
        
            print("request_user_id:",request.user.id)
            project = Project.objects.get(pk=project_id)
            
            print("project_id :",project.id)
            print("user_id :",user_id)


            
      
            print("c'est la avant :",project.project_members.all())
            project.project_members.all()
           
           


        except Project.DoesNotExist:
            return JsonResponse({}, safe=False, status=status.HTTP_404_NOT_FOUND)


    print("fin")
    return JsonResponse(request.data, safe=False, status=status.HTTP_201_CREATED)

"""

"""
@api_view(['DELETE'])
def associate_delete_user_project (request,project_id,user=None):

    
    user_id = request.data.get("user_id")
    print(user_id)
    try:
 
            project = Project.objects.get(pk=project_id)
            
            print("project_id :",project.id)
            print("user_id :",user_id)
            for user in project.project_members.all():
                user = User.objects.get(pk=user_id)

            print("user:",user.id)
           
            print("c'est la avant :",project.project_members.all())
            project.project_members.delete(user_id)
            
            project.save()
            print("c'est la apres :",project.project_members.all())

  
    except Project.DoesNotExist:
        return JsonResponse({}, safe=False, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse(request.data, safe=False, status=status.HTTP_201_CREATED)
"""
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

    print("millieu contrib")

    def get_permissions(self):

        id = self.request.user.id
        print(self.action)
        if self.action in ["delete","update","destroy"] :
            contributor = get_object_or_404(Contributor, pk=self.kwargs["pk"])
            print(contributor.author_user_id.id,id)
            print("fin")
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
     
     
    
    """def get(self, request, project_id, user_id):
       Get Contributors list of project by project_id

        user = request.user

        # project error case : Contributor
        project, error_message, error_code = get_project_and_ensure_access(project_id=project_id, contributor=user)
        if error_code is not None:
            return JsonResponse(error_message, safe=False, status=error_code)

        # get contributors
        project_contributors = Contributor.objects.filter(
            id__in=[contributor.id for contributor in Contributor.objects.filter(project_id=project_id)])
        contributors = self.serializer_class(project_contributors, many=True)
        message = contributors.data
        return JsonResponse(message, safe=False, status=status.HTTP_200_OK)"""



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
            print(issue.author_user_id.id,id)
            print("fin")
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
            print(comment.author_user_id.id,id)
            if id != comment.author_user_id.id :
                raise PermissionDenied()

        return super().get_permissions()
