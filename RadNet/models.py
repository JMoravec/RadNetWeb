from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext as _


class BetaEfficiency(models.Model):
    coefficient = models.FloatField()

    def __unicode__(self):
        return str(self.coefficient)


class AlphaEfficiency(models.Model):
    coefficient = models.FloatField()

    def __unicode__(self):
        return str(self.coefficient)


class Filter(models.Model):
    filter_num = models.IntegerField(unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    sample_time = models.FloatField()
    sample_volume = models.FloatField()
    time_start = models.FloatField()
    alpha_coeff = models.ForeignKey(AlphaEfficiency)
    beta_coeff = models.ForeignKey(BetaEfficiency)

    activity_calculated = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.filter_num) + ': ' + str(self.start_date) + ' - ' + \
            str(self.end_date)


class RawData(models.Model):
    filter = models.ForeignKey(Filter)
    time = models.IntegerField(_("Time (HHMMSS)"))
    alpha_reading = models.FloatField(_("Alpha Reading"))
    beta_reading = models.FloatField(_("Beta Reading"))
    clean_filter_count = models.FloatField(_("Clean Filter Count"))

    def __unicode__(self):
        return str(self.Filter) + ' ' + str(self.time)

    def clean(self):
        if self.filter is None:
            msg = _('Filter is required')
            raise ValidationError(msg)
        if self.time is None:
            msg = _('Time is required')
            raise ValidationError(msg)
        if self.alpha_reading is None:
            msg = _('Alpha Reading is required')
            raise ValidationError(msg)
        if self.beta_reading is None:
            msg = _('Beta Reading is required')
            raise ValidationError(msg)
        if self.clean_filter_count is None:
            msg = _('Clean Filter Coutn is required')
            raise ValidationError(msg)

        if len(str(int(self.time))) != 6:
            msg = _('Time Start must be HHMMSS format')
            raise ValidationError(msg)
