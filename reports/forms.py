import datetime
from django import forms
from pytz import timezone
from django.contrib.admin import widgets

tz = timezone('Australia/Sydney')


class ReportDateForm(forms.Form):
    date_from = forms.DateField(widget=widgets.AdminDateWidget(),
                                label="From", input_formats=['%Y-%m-%d'])
    date_to = forms.DateField(widget=widgets.AdminDateWidget(), label="To")


class ReportPayerForm(ReportDateForm):
    over = forms.IntegerField(initial=60,
                              label="* Quantity of Items with Price Over")
