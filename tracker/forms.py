from django import forms
from .models import MilkEntry
import datetime

class MilkEntryForm(forms.ModelForm):

    MONTH_CHOICES = [
        (i, datetime.date(2000, i, 1).strftime('%B'))
        for i in range(1, 13)
    ]

    YEAR_CHOICES = [
        (y, y) for y in range(2020, datetime.datetime.now().year + 1)
    ]

    month = forms.ChoiceField(choices=MONTH_CHOICES, required=False)
    year = forms.ChoiceField(choices=YEAR_CHOICES, required=False)

    class Meta:
        model = MilkEntry
        fields = ['date', 'quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['date'].widget = forms.DateInput(attrs={'type': 'date'})

