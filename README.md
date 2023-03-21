# Django REST Framework with Timelog App
This is a simple Django REST Framework application that allows authenticated users to manage Projects and Timelogs. Users can create and retrieve Projects, and can also add Timelogs to their assigned Projects

### Installation
Clone this repository to your local machine.
Create and activate a new virtual environment.
Install the required packages using the following command:
pip install -r requirements.txt

Create the necessary database tables by running the following command:
python manage.py migrate

### API Endpoints

#### Projects
GET /api/projects/
This endpoint retrieves a list of all Projects in the database.
Response:
{
    "id": 1,
    "name": "Project 1",
    "description": "This is Project 1",
    "project_id": "P1"
}

POST /api/projects/
This endpoint creates a new Project in the database.
Request example:
{
    "name": "Project 1",
    "description": "This is Project 1",
    "project_id": "P1"
}

Response Example: 
{
    "id": 1,
    "name": "Project 1",
    "description": "This is Project 1",
    "project_id": "P1"
}

GET /api/projects/{project_id}/
This endpoint retrieves a specific Project by its project_id.

Response body
{
    "id": 1,
    "name": "Project 1",
    "description": "This is Project 1",
    "project_id": "P1"
}

PUT /api/projects/{project_id}/
This endpoint updates a specific Project by its project_id.

Request body
{
    "name": "Project 1 updated",
    "description": "This is Project 1 updated",
    "project_id": "P1"
}

Response 
{
    "name": "Project 1 updated",
    "description": "This is Project 1 updated",
    "project_id": "P1"
}

DELETE /api/projects/{project_id}/
This endpoint deletes a specific Project by its project_id.

Response
{
    "message": "success"
}

### Timelogs
GET /api/timelogs/
This endpoint retrieves a list of all Timelogs associated with the authenticated user's allocated project.

Response
[
    {
        "id": 1,
        "user": 1,
        "project": 1,
        "description": "Working on Timelog 1",
        "start_time": "2023-03-21T10:00:00Z",
        "end_time": "2023-03-21T12:00:00Z"
    },
    {
        "id": 2,
        "user": 1,
        "project": 1,
        "description": "Working on Timelog 2",
        "start_time": "2023-03-21T13:00:00Z",
        "end_time": "2023-03-21T15:00:00Z"
    }
]

POST /api/timelogs/
This endpoint creates a new Timelog associated with the authenticated user's allocated project.

Request Body
{
    "user": 1,
    "project_id": 1,
    "description": "Debugging",
    "start_time": "2022-03-20T15:00:00Z",
    "end_time": "2022-03-20T16:00:00Z"
}

Response
{
    "id": 3,
    "user": 1,
    "project": 1,
    "description": "Debugging",
    "start_time": "2022-03-20T15:00:00Z",
    "end_time": "2022-03-20T16:00:00Z"
}
