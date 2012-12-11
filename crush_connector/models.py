from django.db import models
import datetime

# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    address = models.CharField(max_length=200, blank=True, null=True)
    year = models.CharField(max_length=100, blank=True, null=True)
    
    num_crushes_used = models.IntegerField(default=0)
    num_allowed_crushes = models.IntegerField(default=-1) # default value -1 means fall back on the value of Crush.num_allowed_crushes

    def __unicode__(self):
        return self.name


class Crush(models.Model):
    crusher = models.ForeignKey(Person, related_name='crush_crushers')
    crushee = models.ForeignKey(Person, related_name='crush_crushees')
    timestamp = models.DateTimeField()
    active = models.BooleanField(default=True)

    num_allowed_crushes = 3 # number of crushes a person can enter on the form
    def __unicode__(self):
        return "%s likes %s" % (self.crusher, self.crushee)

    def save(self, *args, **kwargs):
        '''On save, update timestamps'''
        if not self.id:
            self.timestamp = datetime.datetime.today()
        super(Crush, self).save(*args, **kwargs)

class RefreshDates(models.Model):
    date = models.DateField()

    def __unicode__(self):
        return "%s" % self.date

class PersonBeenNotified(models.Model):
    '''Make sure we only email a person once when someone has a crush on them. This object gets created when we notify them, so if an object exists with their user name they have been notified.'''
    person = models.ForeignKey(Person)

    def __unicode__(self):
        return '%s - %s' % (self.person.name, self.person.email)
