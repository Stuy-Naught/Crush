from django.contrib import admin
from crush_connector.models import *

admin.site.register(Person)
admin.site.register(Crush)
admin.site.register(CrushHash)
admin.site.register(RefreshDates)
admin.site.register(PersonBeenNotified)
admin.site.register(MutualCrush)
admin.site.register(MutualCrushHash)
