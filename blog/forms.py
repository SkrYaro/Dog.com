from django import forms

from blog.models import Post, Category, Tag, Comment


class ReactCreateForm(forms.ModelForm):

    name = forms.CharField(label="Придумайте назву реакції", max_length=100)
    description = forms.CharField(label="Придумайте опис до реакції", max_length=100)
    category = forms.ModelChoiceField(queryset=Category.objects.all(),label="Для приваблювання підходячих юзерів, будь ласка виберіть категорію" ,required=False)
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(),label="Виберіть тег для пояснення мотивів поста",required=False)
    draft = forms.BooleanField(label="Дороблена версія?", required=False)

    class Meta:
        model = Post
        fields = ["name", "description","react", "category" , "tags", "draft"]


class SketchCreateForm(forms.ModelForm):
    name = forms.CharField(label="Придумайте назву відео", max_length=100)
    description = forms.CharField(label="Придумайте опис до відео", max_length=100)
    img = forms.FileField(label="Загрузіть ваший витвір мистецтва")
    category = forms.ModelChoiceField(queryset=Category.objects.all(),label="Для приваблювання підходячих юзерів, будь ласка виберіть категорію" ,required=False)
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(),label="Виберіть тег для пояснення мотивів поста",required=False)
    draft = forms.BooleanField(label="Дороблена версія?", required=False)
    class Meta:
        model = Post
        fields = ["name", "description", "img", "category", "tags", "draft"]


class VideoCreateForm(forms.ModelForm):
    name = forms.CharField(label="Придумайте назву відео",max_length=100 )

    description = forms.CharField(label="Придумайте опис до відео", max_length=100)
    video = forms.FileField(label="Загрузіть відео")
    category = forms.ModelChoiceField(queryset=Category.objects.all(),label="Для приваблювання підходячих юзерів, будь ласка виберіть категорію" ,required=False)
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(),label="Виберіть тег для пояснення мотивів поста",required=False)
    draft = forms.BooleanField(label="Дороблена версія?", required=False)

    class Meta:
        model = Post
        fields = ["name", "description", "video", "category", "tags" , "draft"]


class ComentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
