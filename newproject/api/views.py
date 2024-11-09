from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializer import UserSerializer
from django.db import transaction

# Create your views here.
@api_view(['GET'])
def get_users(request): # request parameter represent the http request object that contains all the details about the incoming request. It is mandatory to have request parameter in the view function since it will be used by django framework.
    """Get a user from the database"""
    users = User.objects.all() # return list like object containing instance of user model 
    # print(type(users))
    serializer = UserSerializer(users, many=True) # serailize multiple data
    print(type(serializer)) # <class 'rest_framework.utils.serializer_helpers.ReturnList'>
    print(serializer) 
    return Response(serializer.data) # serializer.data returns json/dict structure

@api_view(['POST'])
def create_user(request):
    """Create user and store it in the database"""
    serailizer = UserSerializer(data=request.data) #deserialize data
    print(serailizer)  # type: <class 'api.serializer.UserSerializer'>
    if serailizer.is_valid(): # checking should be done when deserializing. check for datatype, required field, min and max length and custom validation written in serializer class
        serailizer.save()
        return Response(serailizer.data, status=status.HTTP_201_CREATED)
    return Response(serailizer.errors, status=status.HTTP_400_BAD_REQUEST) # after the .is_valid(), 2 things happen 1) updates the validated_data and errors attribute for the serializer instance

@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk):
    """Get, delete, and update a user detail"""
    try:
        user = User.objects.get(id=pk) # return a user object
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
 
    if request.method == "GET":
        serializer = UserSerializer(user) # used to serialize
        print(type(serializer)) # <class 'api.serializer.UserSerializer'>
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == "PUT":
        #serializer = UserSerializer(user, data=request.data) # for put request 2 parameters are always passd. 1st parameter is instance you want to update and 2nd parameter is data from the request.data
        # if serializer.is_valid(): 
        #     serializer.save()
        #     return Response(serializer.data)
        with transaction.atomic():
            serializer = UserSerializer(user)
            user.name = request.data.get("name")
            user.age = request.data.get("age")
            # user.save()
            # raise ValueError("Something went wrong")
        return Response(status=status.HTTP_200_OK)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "DELETE":
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    