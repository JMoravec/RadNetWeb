from django.db import models


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
    time = models.IntegerField()
    alpha_reading = models.FloatField()
    beta_reading = models.FloatField()
    clean_filter_count = models.FloatField()

    def __unicode__(self):
        return str(self.Filter) + ' ' + str(self.time)
