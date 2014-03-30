from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from RadNet.models import Filter, AlphaEfficiency, BetaEfficiency
from django.utils.translation import ugettext as _

__author__ = 'Joshua Moravec'


class FilterForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)
        self.fields['filter_num'].label = _('Filter #:')
        self.fields['start_date'].label = _('Start Date:')
        self.fields['end_date'].label = _('End Date:')
        self.fields['sample_time'].label = _('Sample Time (In Hours):')
        self.fields['sample_volume'].label = _('Sample Volume:')
        self.fields['time_start'].label = _('Time Start (HHMMSS):')
        self.fields['alpha_coeff'].label = _('Alpha Coefficient:')
        self.fields['beta_coeff'].label = _('Beta Coefficient:')

    class Meta:
        model = Filter
        widgets = {
            'end_date': forms.TextInput(attrs={'class': 'datepicker'}),
            'start_date': forms.TextInput(attrs={'class': 'datepicker'}),
        }
        exclude = ['activityCalculated']

    def clean(self):
        cleaned_data = super(ModelForm, self).clean()
        time_start = cleaned_data.get('time_start')
        if len(str(int(time_start))) != 6:
            msg = _('Time Start must be HHMMSS format')
            self._errors['time_start'] = self.error_class([msg])
            del cleaned_data['time_start']
        return cleaned_data


class AlphaCoeffForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(AlphaCoeffForm, self).__init__(*args, **kwargs)
        self.fields['coefficient'].label = _('Alpha Coefficient:')

    class Meta:
        model = AlphaEfficiency


class BetaCoeffForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(BetaCoeffForm, self).__init__(*args, **kwargs)
        self.fields['coefficient'].label = _('Beta Coefficient:')

    class Meta:
        model = BetaEfficiency