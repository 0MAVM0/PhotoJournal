from rest_framework.generics import CreateAPIView
from .serializers import RegisterSerializer
from .models import CustomUser


class RegisterView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
