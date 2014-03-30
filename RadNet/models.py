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

    activityCalculated = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.filter_num) + ': ' + str(self.start_date) + ' - ' + \
            str(self.end_date)




class RawData(models.Model):
    Filter = models.ForeignKey(Filter)
    time = models.IntegerField()
    alphaReading = models.FloatField()
    betaReading = models.FloatField()
    cleanFilterCount = models.FloatField()

    def __unicode__(self):
        return str(self.Filter) + ' ' + str(self.time)

    def clean(self):
        if len(str(int(self.time))) != 6:
            raise ValidationError(_('Time must be HHMMSS format'))