from rest_framework.generics import RetrieveAPIView

from .models import Result
from .serializer import ResultSerializer
from .filter import ResultFilter


class ResultRetrieveView(RetrieveAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    filter_class = ResultFilter

