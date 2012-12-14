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
        return str(self.pk)


class Crush(models.Model):
    crusher = models.ForeignKey(Person, related_name='crush_crushers')
    crushee = models.ForeignKey(Person, related_name='crush_crushees')
    timestamp = models.DateTimeField()
    active = models.BooleanField(default=True)

    num_allowed_crushes = 3 # number of crushes a person can enter on the form
    def __unicode__(self):
        return "%d likes %d" % (self.crusher.pk, self.crushee.pk)

    def save(self, *args, **kwargs):
        '''On save, update timestamps'''
        if not self.id:
            self.timestamp = datetime.datetime.today()
        super(Crush, self).save(*args, **kwargs)

class CrushHash(models.Model):
    crusher = models.ForeignKey(Person)
    digest = models.CharField(max_length=128)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField()
    
    def __unicode__(self):
        if self.active:
            active_str = 'Active'
        else:
            active_str = 'Inactive'
        return '%s (%s): %s' % (active_str, self.timestamp, self.digest)

class RefreshDates(models.Model):
    date = models.DateField()

    def __unicode__(self):
        return "%s" % self.date

class PersonBeenNotified(models.Model):
    '''Make sure we only email a person once when someone has a crush on them. This object gets created when we notify them, so if an object exists with their user name they have been notified.'''
    person = models.ForeignKey(Person)

    def __unicode__(self):
        return '%d' % self.person.pk

class MutualCrushHash(models.Model):

    crush_hash = models.ForeignKey(CrushHash)

    def __unicode__(self):
        return '%s' % self.crush_hash

class MutualCrush(models.Model):

    crush = models.ForeignKey(Crush)

    def __unicode__(self):
        return '%s' % self.crush

    def save(self, *args, **kwargs):
        '''Save this mutual crush, but only if we haven\'t already made a match between these two people.'''
        for mutual in MutualCrush.objects.all():
            if (mutual.crush.crusher == self.crush.crusher and mutual.crush.crushee == self.crush.crushee) \
               or (mutual.crush.crusher == self.crush.crusher and mutual.crush.crushee == self.crush.crushee):
                return
        super(MutualCrush, self).save(*args, **kwargs)
