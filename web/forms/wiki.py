from django import forms
from web import models
from web.forms.BootStrapForm import BootStrapForm


class WikiModelForm(BootStrapForm, forms.ModelForm):

    class Meta:
        model = models.Wiki
        fields = ['title', 'content', 'parent']

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        total_list = [('', '请选择'), ]
        data_list = models.Wiki.objects.filter(project=request.tracer.project).values_list('id', 'title')
        total_list.extend(data_list)

        self.fields['parent'].choices = total_list





