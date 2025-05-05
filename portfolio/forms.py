from django import forms
from portfolio.models import Portfolio, Like


class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ["title", "body", "file"]

    def __init__(self, *args, **kwargs):
        super(PortfolioForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})