from django.db import models


class FX(models.Model):
    rmb = models.DecimalField(max_digits=8, decimal_places=2)
    aud = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date',)
        verbose_name = 'Exchange Record'

    def __str__(self):
        return str(self.date)
