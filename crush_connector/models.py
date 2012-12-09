from django.db import models

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
    timestamp = models.DateTimeField(auto_now=True)

    num_allowed_crushes = 3 # number of crushes a person can enter on the form
    def __unicode__(self):
        return "%s likes %s" % (self.crusher, self.crushee)
