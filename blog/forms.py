from django import forms

from blog.models import Reaction, Sketch, Video


class ReactCreateForm(forms.ModelForm):
    class Meta:
        model = Reaction
        fields = ["name", "description"]


class SketchCreateForm(forms.ModelForm):
    class Meta:
        model = Sketch
        fields = ["name", "description", "img"]


class VideoCreateForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ["name", "description", "video"]

