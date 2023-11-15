from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics, status
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.db.models import Q

from treasury.models import MonthlyBalance

from .serializers import (
    MinuteExcerptsSerializer,
    UsersFunctionsSerializer,
    CustomUserSerializer,
    MeetingMinuteModelSerializer,
    MinuteTemplateModelSerializer,
    TransactionModelSerializer,
    TransactionCatModelSerializer,
    BalanceSerializer,
)
from users.models import UsersFunctions, CustomUser

from secretarial.models import MinuteExcerptsModel
from secretarial.models import MeetingMinuteModel, MinuteTemplateModel

from treasury.models import TransactionModel


@api_view(["GET"])
def getCurrentBalance(request):
    current_month = timezone.now().month
    current_year = timezone.now().year

    previous_month = timezone.now() - relativedelta(months=1)

    last_month_balance = MonthlyBalance.objects.get(month__month=previous_month.month, month__year=previous_month.year)

    transactions_queryset = TransactionModel.objects.filter(
        date__month=current_month, date__year=current_year
    ).order_by("-date")

    positive_transactions_queryset = transactions_queryset.filter(is_positive=True)
    negative_transactions_queryset = transactions_queryset.filter(is_positive=False)

    unaware_month_balance = sum(t.amount for t in transactions_queryset)
    positive_transactions = sum(pt.amount for pt in positive_transactions_queryset)
    negative_transactions = sum(nt.amount for nt in negative_transactions_queryset)

    aware_month_balance = last_month_balance.balance + unaware_month_balance

    serializer = BalanceSerializer(
        {
            "current_balance": aware_month_balance,
            "last_month_balance": last_month_balance.balance,
            "unaware_month_balance": unaware_month_balance,
            "sum_negative_transactions": negative_transactions,
            "sum_positive_transactions": positive_transactions,
        }
    )

    return Response(serializer.data)


@api_view(["GET"])
def getData(request):
    excerpts = MinuteExcerptsModel.objects.all()
    serializer = MinuteExcerptsSerializer(excerpts, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getDetailedData(request, pk):
    excerpt = MinuteExcerptsModel.objects.get(pk=pk)
    excerpt.times_used += 1
    excerpt.save()
    serializer = MinuteExcerptsSerializer(excerpt, many=False)
    return Response(serializer.data)


@api_view(["GET"])
def getUserFunction(request, pk):
    user_roles = UsersFunctions.objects.filter(member=pk)
    serializer = UsersFunctionsSerializer(user_roles, many=True)
    return Response(serializer.data)


class SearchUsersListCreateAPIView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def post(self, request, *args, **kwargs):
        search_criterion = request.data.get("searched")
        queryset = CustomUser.objects.filter(
            Q(first_name__icontains=search_criterion)
            | Q(last_name__icontains=search_criterion)
        )
        serialized_data = CustomUserSerializer(queryset, many=True)
        return Response(serialized_data.data)


class SearchMembersListCreateAPIView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.filter(
        Q(type=CustomUser.Types.REGULAR) | Q(type=CustomUser.Types.STAFF)
    )
    serializer_class = CustomUserSerializer

    def post(self, request, *args, **kwargs):
        search_criterion = request.data.get("searched")
        queryset = self.queryset.filter(
            Q(first_name__icontains=search_criterion)
            | Q(last_name__icontains=search_criterion)
        )
        serialized_data = CustomUserSerializer(queryset, many=True)
        return Response(serialized_data.data)


class SearchMinutesListCreateAPIView(generics.ListCreateAPIView):
    queryset = MeetingMinuteModel.objects.all()
    serializer_class = MeetingMinuteModelSerializer

    def post(self, request, *args, **kwargs):
        search_criterion = request.data.get("searched")
        queryset = MeetingMinuteModel.objects.filter(body__icontains=search_criterion)
        serialized_data = MeetingMinuteModelSerializer(queryset, many=True)
        return Response(serialized_data.data)


class SearchTemplatesListCreateAPIView(generics.ListCreateAPIView):
    queryset = MinuteTemplateModel.objects.all()
    serializer_class = MinuteTemplateModelSerializer

    def post(self, request, *args, **kwargs):
        search_criterion = request.data.get("searched")
        queryset = MinuteTemplateModel.objects.filter(
            Q(title__icontains=search_criterion) | Q(body__icontains=search_criterion)
        )
        serialized_data = MinuteTemplateModelSerializer(queryset, many=True)
        return Response(serialized_data.data)


class TransactionCatListAPIView(generics.ListAPIView):
    serializer_class = TransactionCatModelSerializer

    def get_queryset(self):
        current_month = timezone.now().month
        current_year = timezone.now().year

        queryset = TransactionModel.objects.filter(
            date__month=current_month, date__year=current_year
        ).order_by("-date")
        return queryset


class TransactionsCreateAPIView(generics.CreateAPIView):
    serializer_class = TransactionModelSerializer

    def post(self, request, *args, **kwargs):
        serializer = TransactionModelSerializer(data=request.data)
        print("DADOS ENVIADOS:", request.data)

        # Validate the data
        if serializer.is_valid():
            # Create and save a new instance
            serializer.save()

            # Serialize the saved instance
            serialized_data = TransactionCatModelSerializer(serializer.instance)

            # Return a successful response with the serialized data
            return Response(serialized_data.data, status=status.HTTP_201_CREATED)
        else:
            # If data is not valid, return a response with error details
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteTransaction(generics.DestroyAPIView):
    queryset = TransactionModel.objects.all()
    serializer_class = TransactionModelSerializer
