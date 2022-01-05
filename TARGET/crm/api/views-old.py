# generic
from django.views.decorators.csrf import csrf_exempt

from ..models import Product, Channel, Country, Area, City
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from .serializers import CountrySerializer, AreaSerializer, CitySerializer
from rest_framework.response import Response
from rest_framework import status, generics, mixins, viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView

# class CountryViewSet(viewsets.ViewSet):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#
#     def list(self, request):
#         countries = Country.objects.all()
#         serializer = CountrySerializer(countries, many=True)
#         return Response(serializer.data)
#
#     def create(self, request):
#         serializer = CountrySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def retrieve(self, request, pk=None):
#         queryset = Country.objects.all()
#         countries = get_object_or_404(queryset, pk=pk)
#         serializer = CountrySerializer(countries)
#         return Response(serializer.data)
#
#     def update(self, request, pk=None):
#         countries = Country.objects.get(pk=pk)
#         serializer = CountrySerializer(countries, data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def destroy(self, request, pk=None):
#         countries = Country.objects.get(pk=pk)
#         countries.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

class AreaViewSet(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Area.objects.all()
    serializer_class = AreaSerializer

class CityViewSet(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = City.objects.all()
    serializer_class = CitySerializer



# class CountryGenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
#     serializer_class = CountrySerializer
#     queryset = Country.objects.all()
#     lookup_field = 'id'
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request, id=None):
#         if id:
#             return self.retrieve(request)
#         else:
#             return self.list(request)
#
#     def post(self, request):
#         return self.create(request)
#
#     def put(self, request, id=None):
#         return self.update(request, id)
#
#     def delete(self, request, id):
#         return self.destroy(request, id)



# class CountryAPIView(APIView):
#     def get(self, request):
#         countries = Country.objects.all()
#         serializer = CountrySerializer(countries, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = CountrySerializer(data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class CountryDetails(APIView):
#     def get_object(self, id):
#         try:
#             return Country.objects.get(id=id)
#         except Country.DoesNotExist:
#             return HttpResponse(status=status.HTTP_404_NOT_FOUND)
#
#     def get(self, request, id):
#         countries = self.get_object(id)
#         serializer = CountrySerializer(countries)
#         return Response(serializer.data)
#
#     def put(self, request, id):
#         countries = self.get_object(id)
#         serializer = CountrySerializer(countries, data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, id):
#         countries = self.get_object(id)
#         countries.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#


# # @csrf_exempt
# @api_view(['GET', 'POST'])
# def country_list(request):
#     if request.method == 'GET':
#         countries = Country.objects.all()
#         serializer = CountrySerializer(countries, many=True)
#         # return JsonResponse(serializer.data, safe= False)
#         return Response(serializer.data)
#
#
#     elif request.method == 'POST':
#         # data = JSONParser().parse(request)
#         serializer = CountrySerializer(data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# def country_details(request, pk):
#     try:
#         countries = Country.objects.get(pk=pk)
#     except Country.DoesNotExist:
#         return HttpResponse(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == "GET":
#         serializer = CountrySerializer(countries)
#         return Response(serializer.data)
#
#     elif request.method == 'PUT':
#         serializer = CountrySerializer(countries, data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         countries.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
