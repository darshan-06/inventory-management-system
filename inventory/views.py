from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from .models import Item
from .serializers import ItemSerializer, RegisterUserSerializer
from django.core.cache import cache
from rest_framework.views import APIView


@api_view(['POST'])
def register_user(request):
    serializer = RegisterUserSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data

    if User.objects.filter(username=data['username']).exists():
        return Response({'status':'error','message': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.create(
        username=data['username'],
        password=make_password(data['password']) 
    )
    
    return Response({'status':'ok','message': 'User registered successfully'}, status=status.HTTP_201_CREATED)




class ItemView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        if Item.objects.filter(name=data['name']).exists():
            return Response({'status': 'error', 'message': 'Product already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(data, status=status.HTTP_201_CREATED)


    def get(self, request, item_id):
        item = cache.get(item_id)
        if not item:
            try:
                item = Item.objects.get(id=item_id)
                cache.set(item_id, item)
            except Item.DoesNotExist:
                return Response({'status': 'error', 'message': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ItemSerializer(item)
        return Response(serializer.data)


    def put(self, request, item_id):
        try:
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            return Response({'status': 'error', 'message': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.set(item_id, serializer.data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, item_id):
        try:
            item = Item.objects.get(id=item_id)
            item.delete()
            cache.delete(item_id)
            return Response({'status': 'ok', 'message': 'Item deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Item.DoesNotExist:
            return Response({'status': 'error', 'message': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
