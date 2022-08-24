from django.contrib import admin
from .models import Account, Session, Action, Accrual, Payment


admin.site.register(Account)
admin.site.register(Session)
admin.site.register(Action)
admin.site.register(Accrual)
admin.site.register(Payment)