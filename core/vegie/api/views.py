from .serializers import ReceipeSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins
from rest_framework import generics
from .permissions import CustomPermission
from ..models import Receipe
from rest_framework_simplejwt.authentication import JWTAuthentication


class ReceipeList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomPermission]
    queryset = Receipe.objects.all()
    serializer_class = ReceipeSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        request.data['user'] = request.user
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReceipeDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomPermission]
    queryset = Receipe.objects.all()
    serializer_class = ReceipeSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

# @api_view(['GET', 'POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def api_receipes(request):
#     if request.method == 'GET':
#         receipes = Receipe.objects.all()
#         serializer = ReceipeSerializer(receipes, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif request.method == 'POST':
        
#         serializer = ReceipeSerializer(data=request.data)

#         if serializer.is_valid():
#             print(serializer.validated_data)
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(["GET", "PUT", "DELETE"])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def api_detail_receipes(request, id):
#     if request.method == 'GET':
#         receipe = Receipe.objects.get(id=id)
#         serializer = ReceipeSerializer(receipe, many=False)
#         return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'PUT':
#         receipe = Receipe.objects.get(id=id)
#         serializer = ReceipeSerializer(receipe, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD)
#     elif request.method == 'DELETE':
#         receipe = Receipe.objects.get(id=id)
#         receipe.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
