from crush_connector.models import Person, Crush, CrushHash, PersonBeenNotified
from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
  def handle_noargs(self, *args, **kwargs):
    tester_1 = Person.objects.get(email='eliasb@mit.edu')
    tester_2 = Person.objects.get(email='whaack@mit.edu')
    crushes_1 = Crush.objects.filter(crusher=tester_1)
    crushes_2 = Crush.objects.filter(crusher=tester_2)
    for crush in crushes_1:
      crush.delete()
    for crush in crushes_2:
      crush.delete()

    crush_hashes_1 = CrushHash.objects.filter(crusher=tester_1)
    crush_hashes_2 = CrushHash.objects.filter(crusher=tester_2)
    for crush in crush_hashes_1:
      crush.delete()
    for crush in crush_hashes_2:
      crush.delete()
    
    notified_1 = PersonBeenNotified.objects.filter(person=tester_1)
    notified_2 = PersonBeenNotified.objects.filter(person=tester_2)
    for notified in notified_1:
      notified.delete()
    for notified in notified_2:
      notified.delete()

    tester_1.num_crushes_used = 0
    tester_2.num_crushes_used = 0
    tester_1.save()
    tester_2.save()
