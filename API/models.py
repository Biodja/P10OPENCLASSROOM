from django.db import models
from django.db.models import ForeignKey, CharField
from django.contrib.auth import get_user_model
from django.db.models import DateTimeField

class Project(models.Model):
    title = CharField(max_length=128)
    description = CharField(max_length=2048)
    type = CharField(max_length=128)
    author_user_id = ForeignKey(get_user_model() , on_delete=models.CASCADE)
    project_members = models.ManyToManyField(get_user_model() , through='Contributor' , related_name='project_contributor')

class Contributor(models.Model):
    user_id = ForeignKey(get_user_model() , on_delete=models.CASCADE)
    project_id = ForeignKey(Project , on_delete=models.CASCADE)

    class PermissionChoices(models.TextChoices):
        niveau_1 = "1", "Utilisateur"
        niveau_2 = "2", "Contributeur"
        niveau_3 = "3", "Manager"
    permission = models.CharField(max_length=1 ,choices=PermissionChoices.choices ,default=PermissionChoices.niveau_1)
    role = CharField(max_length=128)
    

class Issue(models.Model):
    class PriorityChoices(models.TextChoices):
        niveau_1 = "1", "Pas Urgent"
        niveau_2 = "2", "Urgent"
        niveau_3 = "3", "Très Urgent"

        
    class TagChoices(models.TextChoices):
        niveau_1 = "1", "Bugg"
        niveau_2 = "2", "Amélioration"
        niveau_3 = "3", "Taches"
    title = CharField(max_length=128)
    desk = CharField(max_length=300)
    tag = CharField(max_length=128)
    priority = CharField(max_length=128,choices=PriorityChoices.choices, default=PriorityChoices.niveau_1)
    project_id = ForeignKey(to=Project ,on_delete=models.CASCADE)
    status = CharField(max_length=128)
    author_user_id = ForeignKey(get_user_model(),on_delete=models.CASCADE)
    assignee_user_id = ForeignKey(get_user_model(), on_delete=models.CASCADE , related_name='assigned_issue')
    created_time = DateTimeField(auto_now_add=True)
    issue_comment = models.ManyToManyField(get_user_model(), through='Comment', related_name='issue_comment')

class Comment(models.Model):
    description = CharField(max_length=128)
    author_user_id = ForeignKey(get_user_model(), on_delete=models.CASCADE)
    issue_id = ForeignKey(Issue ,on_delete=models.CASCADE)
    created_time = DateTimeField(auto_now_add=True)