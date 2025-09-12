from django import forms
from panel.models import Speak, Dialog


class MessageForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    class Meta:
        model = Speak
        fields = ["writes","image"]


class DialogForm(forms.ModelForm):
    class Meta:
        model = Dialog
        fields = ["title"]
