from django.db import models

# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()

class Crush(models.Model):
    crusher = models.ForeignKey(Person, related_name='crush_crushers')
    crushee = models.ForeignKey(Person, related_name='crush_crushees')
