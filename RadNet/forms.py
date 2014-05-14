from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from RadNet.models import Filter, AlphaEfficiency, BetaEfficiency, RawData
from django.utils.translation import ugettext as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Fieldset, HTML
from crispy_forms.bootstrap import StrictButton, FormActions, FieldWithButtons

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

    helper = FormHelper()
    helper.form_action = 'addFilter'
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-lg-3 col-sm-4'
    helper.field_class = 'col-lg-6 col-sm-4'
    helper.layout = Layout(
        'filter_num',
        'start_date',
        'end_date',
        'sample_time',
        'sample_volume',
        'time_start',
        'alpha_coeff',
        'beta_coeff',
        StrictButton(_('Create Filter'), type='submit', css_class='btn-default'),
    )

    class Meta:
        model = Filter
        widgets = {
            'end_date': forms.TextInput(attrs={'class': 'datepicker'}),
            'start_date': forms.TextInput(attrs={'class': 'datepicker'}),
        }
        exclude = ['activity_calculated']

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

    helper = FormHelper()
    helper.form_action = '/Data/AddCoefficients/1/'
    helper.form_class = 'form-inline'
    helper.field_template = 'bootstrap3/layout/inline_field.html'
    helper.layout = Layout(
        FieldWithButtons('coefficient',
                         StrictButton(_('Add Alpha Coefficient'), type='submit', css_class='btn-default')),
    )

    class Meta:
        model = AlphaEfficiency
help_text_inline = False


class BetaCoeffForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(BetaCoeffForm, self).__init__(*args, **kwargs)
        self.fields['coefficient'].label = _('Beta Coefficient:')

    helper = FormHelper()
    helper.form_action = '/Data/AddCoefficients/2/'
    helper.form_class = 'form-inline'
    helper.field_template = 'bootstrap3/layout/inline_field.html'
    helper.layout = Layout(
        FieldWithButtons('coefficient',
                         StrictButton(_('Add Beta Coefficient'), type='submit', css_class='btn-default')),
    )

    class Meta:
        model = BetaEfficiency


class RawDataForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(RawDataForm, self).__init__(*args, **kwargs)
        self.fields['filter'].label = _('Filter:')
        self.fields['time'].label = _('Time (HHMMSS):')
        self.fields['alpha_reading'].label = _('Alpha Reading:')
        self.fields['beta_reading'].label = _('Beta Reading:')
        self.fields['clean_filter_count'].label = _('CFC:')

    class Meta:
        model = RawData

    def clean(self):
        cleaned_data = super(ModelForm, self).clean()
        time = cleaned_data('time')
        if len(str(int(time))) != 6:
            msg = _('Time Start must be HHMMSS format')
            self._errors['time'] = self.error_class([msg])
            del cleaned_data['time']
        return cleaned_data


class RawDataFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(RawDataFormSetHelper, self).__init__(*args, **kwargs)
        self.form_method = 'post'
        self.form_class = 'form-inline'
        self.field_template = 'bootstrap3/layout/inline_field.html'
        #self.field_template = 'bootstrap/table_inline_formset.html'
        self.layout = Layout(
            HTML("{{ forloop.counter }}:"),
            'time',
            'alpha_reading',
            'beta_reading',
            'clean_filter_count',
            HTML("<br /><br />"),
        )


class NumberOfRawData(forms.Form):
    rows = forms.ChoiceField(choices=[(x, x) for x in range(1, 21)])
    rows.label = _('Number of Rows:')
    rows.required = True

    filters = forms.ModelChoiceField(queryset=Filter.objects.all())
    filters.label = _('Filter:')
    filters.required = True

    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-md-3'
    helper.field_class = 'col-md-6'
    helper.layout = Layout(
        'filters',
        'rows',
        StrictButton(_('Get Data'), type='submit', css_class='btn-default')
    )
