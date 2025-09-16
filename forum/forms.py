from django import forms

from forum.models import Forum


class BlankForm(forms.ModelForm):
    img = forms.ImageField(required=False,label="фото")
    class Meta:
        model = Forum
        fields = ["title", "text","img" ]
