from django.db.models import Max, Count
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Action, Account, Accrual, Payment
from .serializers import AccountSerializer


class AccountViewSet(viewsets.ReadOnlyModelViewSet):
    """Task one"""
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


class AccrualView(APIView):
    """Task two"""

    def get(self, request):
        # result = {}
        # accruals = list(Accrual.objects.all())
        # payments = Payment.objects.all()
        # for pay in payments:
        #     for accrual in accruals:
        #         if pay.date.month == accrual.date.month:
        #             result[f'платеж {pay.date}'] = f'долг {accrual.date}'
        #             accruals.remove(accrual)
        #             break
        #         result[f'платеж {pay.date}'] = 'нет долга для этого платежа'
        # return Response(result, status=status.HTTP_200_OK)

        # TODO тут думал просто сортированные долги и платежи объединить в словарь,
        # самый ранний платеж к самому раннему долгу
        result = {}
        accruals = list(Accrual.objects.all())
        payments = list(Payment.objects.all())
        for pay in payments:
            for accrual in accruals:
                if pay.date.month == accrual.date.month:
                    result[f'платеж {pay.date} id {pay.pk}'] = f'долг {accrual.date} id {accrual.pk}'
                    accruals.remove(accrual)
                    break
            if f'платеж {pay.date} id {pay.pk}' not in result.keys():
                result[f'платеж {pay.date} id {pay.pk}'] = 'нет долга для этого платежа'
        return Response(result, status=status.HTTP_200_OK)