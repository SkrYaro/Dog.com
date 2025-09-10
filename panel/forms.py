from django import forms
from panel.models import Speak, Dialog


class MessageForm(forms.ModelForm):
    img = forms.ImageField(required=False)
    class Meta:
        model = Speak
        fields = ["writes","img"]


class DialogForm(forms.ModelForm):
    class Meta:
        model = Dialog
        fields = ["title"]
