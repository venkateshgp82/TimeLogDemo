from django.contrib.auth.models import User
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import ValidationError, NotFound, NotAcceptable
from .models import Project, Timelog, UserProfile

from .serializers import ProjectSerializer, TimelogSerializer, UserProfileSerializer

# Create your views here.

class ProjectView(APIView):
    """
This APIView allows authenticated users to retrieve and create Project objects.

Authentication:
SessionAuthentication: Uses Django session authentication for authentication
BasicAuthentication: Uses basic authentication for authentication

Permissions:
IsAuthenticated: Only authenticated users can access this API.

GET request:
Returns a list of all Project objects in the database as serialized data.

POST request:
Creates a new Project object in the database with the data provided in the request.
Returns the serialized data of the newly created Project object.
If a Project with the same project_id already exists, a ValidationError is raised.
"""
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        queryset = Project.objects.all()
        serializer = ProjectSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        try:
            serializer = ProjectSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except Exception as e:
            raise ValidationError(f'Project is already present with project ID: {request.data.get("project_id")}')
        
class ProjectDetail(APIView):
    """
This APIView class allows authenticated users to retrieve, update, and delete Project objects by their project_id.

Authentication:

SessionAuthentication: Uses Django session authentication for authentication
BasicAuthentication: Uses basic authentication for authentication
Permissions:

IsAuthenticated: Only authenticated users can access this API.
GET request:

Retrieves a specific Project object by its project_id.
Returns the serialized data of the retrieved Project object.
If the project_id is not found, a NotFound exception is raised.
PUT request:

Updates a specific Project object by its project_id with the data provided in the request.
Returns the serialized data of the updated Project object.
If the project_id is not found, a NotFound exception is raised.
DELETE request:

Deletes a specific Project object by its project_id.
Returns a success message if the deletion is successful.
If the project_id is not found, a NotFound exception is raised.
"""
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):
        try:
            project = Project.objects.get(project_id=project_id)
            serializer = ProjectSerializer(project)
            return Response(serializer.data)
        except Exception as e:
            raise NotFound(f'Project not found with ID: {project_id}')

    def put(self, request, project_id):
        try:
            project = Project.objects.get(project_id=project_id)
            serializer = ProjectSerializer(project, request.data)
            return Response(serializer.data)
        except Exception as e:
            raise NotFound(f'Project not found with ID: {project_id}')
    
    def delete(self, requests, project_id):
        try:
            Project.objects.get(project_id=project_id).delete()
            return Response({'message':'success'})
        except Exception as e:
            raise NotFound(f'project not found') 

class TimelogView(APIView):
    """
This APIView class allows authenticated users to retrieve and create Timelog objects for their allocated project.

Authentication:

SessionAuthentication: Uses Django session authentication for authentication
BasicAuthentication: Uses basic authentication for authentication
Permissions:

IsAuthenticated: Only authenticated users can access this API.
GET request:

Retrieves all Timelog objects associated with the authenticated user's allocated project.
Returns the serialized data of the retrieved Timelog objects.
If the project_id for the authenticated user is not found, a NotFound exception is raised.
If the user is not found, a NotFound exception is raised.
POST request:

Adds a new Timelog object to the authenticated user's allocated project.
Returns the serialized data of the newly created Timelog object.
Only the authenticated user can add timelogs for their own user ID.
If the user tries to add a timelog for a project that is not their allocated project, a NotAcceptable exception is raised.
If there is any error during validation or saving of the new Timelog object, a ValidationError is raised with details of the error and the request data.
"""
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
#    request.user == request.data.get('user')
    def get(self, request):
        try:
            project_id = UserProfile.objects.get(user__username=request.user).project.project_id
            if project_id is None:
                raise NotFound('Project_id not found for the user.')
            queryset = Timelog.objects.filter(project__project_id=project_id)
            serializer = TimelogSerializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            raise NotFound('User not found')

    def post(self, request):
        """
        User only can add timelogs to his assigned project as mentione in UserProfile model
        """
        try:
            username = User.objects.get(id=request.data.get('user')).username
            if str(request.user).strip().lower() != username.strip().lower():
                raise NotAcceptable(f'You can only add your own timelogs')
            
            allocated_project_id = UserProfile.objects.get(user__username=request.user).project.id
            if allocated_project_id != request.data.get('project'):
                raise NotAcceptable(f'User {request.user} can only add time logs for his allocated project only')
            else:
                serializer = TimelogSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)
        except Exception as e:
            raise ValidationError({'error': str(e), 'data': request.data})

class TimelogDetail(APIView):
    """
This APIView class allows authenticated users to edit and delete their own Timelog objects by their id (pk).

Authentication:

SessionAuthentication: Uses Django session authentication for authentication
BasicAuthentication: Uses basic authentication for authentication
Permissions:

IsAuthenticated: Only authenticated users can access this API.
PUT request:

Edits a specific Timelog object by its id with the data provided in the request.
Only allows editing of the timelog if it belongs to the authenticated user.
Only allows editing of timelogs for the authenticated user's allocated project.
Returns the serialized data of the updated Timelog object.
If the user is not authorized or the timelog id is not found, a ValidationError exception is raised.
DELETE request:

Deletes a specific Timelog object by its id.
Only allows deleting of the timelog if it belongs to the authenticated user.
Returns a success message if the deletion is successful.
If the user is not authorized or the timelog id is not found, a ValidationError exception is raised.
"""
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def put(self, request, pk):
        """
        Edit api to edit logged in user log only
        """
        try:
            username = User.objects.get(id=request.data.get('user')).username
            if str(request.user).strip().lower() != username.strip().lower():
                raise NotAcceptable(f'You can only edit your own timelogs')
            
            allocated_project_id = UserProfile.objects.get(user__username=request.user).project.id
            if allocated_project_id != request.data.get('project'):
                raise NotAcceptable(f'User {request.user} can only add time logs for his allocated project only')
            else:
                timelog = Timelog.objects.get(id=pk)
                serializer = TimelogSerializer(timelog, request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)
        except Exception as e:
            raise ValidationError({'error': str(e), 'data': request.data})
    
    def delete(self, request, pk):
        try:
            username = User.objects.get(id=request.data.get('user')).username
            if str(request.user).strip().lower() != username.strip().lower():
                raise NotAcceptable(f'You can only delete your own timelogs')
            
            else:
                timelog = Timelog.objects.get(id=pk)
                Timelog.objects.get(id=pk).delete()
                return Response({"message":"success"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            raise ValidationError({'error': str(e), 'data': request.data})


        
class UserProfileView(APIView):
    """
    API to manage to tag user to a project
    """
    def post(self, request):
        try:
            serializer = UserProfileSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except Exception as e:
            print(str(e))
            raise ValidationError(f'Tagging failed, please check you have entered right username and project_id')