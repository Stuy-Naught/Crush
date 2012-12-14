from crush_connector.models import Crush, MutualCrush
from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
  def handle_noargs(self, *args, **kwargs):
    for crush1 in Crush.objects.all():
      for crush2 in Crush.objects.all():
        if crush1.crusher == crush2.crushee and crush2.crusher == crush1.crushee:
          mutual = MutualCrush(crush=crush1) #, time_delta=crush1.timestamp)
          mutual.save()
