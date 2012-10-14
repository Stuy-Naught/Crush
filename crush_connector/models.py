from django.db import models

# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Crush(models.Model):
    crusher = models.ForeignKey(Person, related_name='crush_crushers')
    crushee = models.ForeignKey(Person, related_name='crush_crushees')

    def __str__(self):
        return "%s likes %s" % (self.crusher, self.crushee)
