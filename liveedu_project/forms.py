from django.forms import ModelForm
from liveedu_project.models import Project


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description']
