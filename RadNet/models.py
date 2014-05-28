from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext as _
from RadNet.time_to_hours import time_to_hours


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
    beta_reading = models.FloatField(_("Beta/Alpha Reading"))
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


class Activity(models.Model):
    filter = models.ForeignKey(Filter)
    raw_data = models.ForeignKey(RawData)
    delta_t = models.FloatField()
    alpha_activity = models.FloatField()
    beta_activity = models.FloatField()

    net_alpha_beta = models.FloatField()
    net_beta = models.FloatField()

    def fill_data(self):
        start_time = time_to_hours(str(self.filter.time_start))
        raw_time = time_to_hours(str(self.raw_data.time))
        #assumes raw time is on the next day here
        if raw_time < start_time:
            raw_time += 24.0

        self.delta_t = raw_time - start_time
        self.net_alpha_beta = self.raw_data.beta_reading - self.raw_data.clean_filter_count
        self.net_beta = self.net_alpha_beta - self.raw_data.alpha_reading
        self.alpha_activity = self.raw_data.alpha_reading * self.filter.alpha_coeff.coefficient
        self.beta_activity = self.net_beta * self.filter.beta_coeff.coefficient


class AlphaCurve(models.Model):
    filter = models.ForeignKey(Filter)
    alpha_1 = models.FloatField()
    alpha_1_lambda = models.FloatField()
    alpha_2 = models.FloatField()
    alpha_2_lambda = models.FloatField()

    def __unicode__(self):
        return str(self.filter) + '\n' + str(self.alpha_1) + '\n' + \
            str(self.alpha_1_lambda) + '\n' + str(self.alpha_2) + '\n' + \
            str(self.alpha_2_lambda)


class BetaCurve(models.Model):
    filter = models.ForeignKey(Filter)
    beta_1 = models.FloatField()
    beta_1_lambda = models.FloatField()
    beta_2 = models.FloatField()
    beta_2_lambda = models.FloatField()

    def __unicode__(self):
        return str(self.filter) + '\n' + str(self.beta_1) + \
            '\n' + str(self.beta_1_lambda) + '\n' + str(self.beta_2) + \
            '\n' + str(self.beta_2_lambda)