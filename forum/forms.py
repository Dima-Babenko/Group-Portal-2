from django import forms
from forum.models import Branch, Comment


class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ["title", "body"]

    def __init__(self, *args, **kwargs):
        super(BranchForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['content', 'media']
        widgets = {
            "media": forms.FileInput()
        }