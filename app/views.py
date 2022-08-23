from django.db.models import Max, Count
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Action, Account
from .serializers import AccountSerializer


class AccountViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()

    @action(detail=True, methods=['GET'])
    def account_actions(self, request, pk):
        # сам запрос
        queryset = Action.objects.filter(session__account__number=self.get_object().number)\
            .values('session__account__id', 'type')\
            .annotate(
            last=Max('created_at'),
            count=Count('type')
        )
        # дальше начинается костыль
        account = self.get_object()
        action = []
        for obj in queryset:
            action.append(
                {
                    'type': obj['type'],
                    'last': obj['last'],
                    'count': obj['count']
                 }
            )
        result = {'number': account.number, 'action': action}
        return Response({'result': result}, status=status.HTTP_200_OK)
