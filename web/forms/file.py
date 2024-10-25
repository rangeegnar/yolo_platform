from django import forms
from web import models
from web.forms.BootStrapForm import BootStrapForm


class FileModelForm(BootStrapForm, forms.ModelForm):

    class Meta:
        model = models.FileInfo
        fields = []

    def __init__(self, *args, **kwargs):
        super(FileModelForm, self).__init__(*args, **kwargs)
        # 如果需要可以自定义更多字段的样式或行为
