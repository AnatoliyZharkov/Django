from django.contrib import admin

from .models import Department, Positions, Worker, PosHistory, VacHistory

admin.site.register(Department)
admin.site.register(Positions)
admin.site.register(Worker)
admin.site.register(PosHistory)
admin.site.register(VacHistory)
