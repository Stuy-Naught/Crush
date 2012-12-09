from crush_connector.models import Person, Crush
from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
    help = "Generate list of names and emails for autocomplete"
    def handle_noargs(self, **options):
        persons = Person.objects.all()
        print("[")
        first = True
        for person in persons:
            if (not first):
                print(",")
            first = False
            print('{"label": "' + person.name + " - " + person.email + '", "value": "' + person.email + '"}')
        print("]")

