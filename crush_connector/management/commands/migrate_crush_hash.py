from crush_connector.models import Person, Crush, CrushHash, MutualCrushHash
from crush_connector.views import isMatch
from crush_connector.hash_crushes import crush_digest
from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
  def handle_noargs(self, *args, **kwargs):
    crushes = Crush.objects.all()
    for crush in crushes:
      digest = crush_digest(crush.crusher, crush.crushee)
      crush_hash = CrushHash(crusher=crush.crusher, digest=digest, timestamp=crush.timestamp)
      crush_hash.save()
      if isMatch(crush.crusher, crush.crushee):
        mutual = MutualCrushHash(crush_hash=crush_hash)
        mutual.save()
