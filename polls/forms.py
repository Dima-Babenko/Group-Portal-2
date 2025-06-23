from django import forms
from .models import PollAnswer, PollOption


class PollAnswerForm(forms.Form):
    selected_option = forms.ModelChoiceField(queryset=PollOption.objects.none(), widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        poll_page = kwargs.pop('poll_page', None)
        super().__init__(*args, **kwargs)
        if poll_page:
            self.fields['selected_option'].queryset = PollOption.objects.filter(poll_page=poll_page)
