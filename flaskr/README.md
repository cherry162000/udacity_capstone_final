### Casting Agency - Udacity FullStack WebDevelopment Project


## Project Motivation
The Casting Agency is a project which helps the producers or directors to add a new movie and the data of the actors and also helping the producers to assign the movies to the particular actors.

This project has API's which demonstrates the CRUD operations on the movies and actors data along with a specified set of roles and permissions limiting the access of data according to the roles assigned to the user. This project uses Auth0 for JWT based authentication.

# Dependencies:

We can install the dependencies using the following command:

pip3 install -r requirements.txt

This project uses SQLAlchemy as backend database to store and retrive the data of the movies and actors.

This project is hosted on a cloud plaftform called Render.

This project uses Auth0 for authentication and added users and roles under that users, which consists of set of permissions which limits the access of the data.

Auth0 Deployment:
1. Login to Auth0 URL : https://auth0.com/
2. Create an account in the Auth0, and navigate to Applications tab and create a new application.
3. Navigate to API's tab and create a new api for the project.
4. Go to roles tab and create the following roles and add the permissions:
  -Casting Assitant:
       get:movies
       get:actors
  -Casting Director:
      get:movies
      get:actors 
      post:movies
      post:actors
  -Casting Producer:
      get:movies
      get:actors 
      post:movies
      post:actors
      patch:movies
      patch:actors
      delete:movies
      delete:actors
5. You can access the JWT token via the following url:
   https://{{YOUR_DOMAIN}}/authorize?audience={{API_IDENTIFIER}}&response_type=token&client_id={{YOUR_CLIENT_ID}}&redirect_uri={{YOUR_CALLBACK_URI}}         

# Models:
* This project has 2 database models
  -Movies which consists of the movie title and the release date
  -Actors which consists of name, age, gender and movie_id(Foreign key) to link the associated movies

## Documenting Endpoints

You will need to provide detailed documentation of your API endpoints including the URL, request parameters, and the response body. Use the example below as a reference.


`GET /movies'`
Example: curl http://127.0.0.1:5000/movies
* This requires permission `get:movies`
* Fetches a dictionary of movies in which the keys are the ids and the value is the corresponding string of the movies
* Request Arguments: None
* Returns: An object with a single key, `movies`, that contains an object of list of actors of that movie, id and release date.

```json
{
    "movies": [
        {
            "actors": [],
            "id": 1,
            "release_date": "4-APR",
            "title": "title7"
        }
    ],
    "success": true
}
```
`GET /actors'`
Example: curl http://127.0.0.1:5000/actors
* This requires permissions `get:actors`
* Fetches a dictionary of actors along with the movie id they are part of
* Request Argguments: None
* Returns: A Json Object which contains name,age,gender and movie_id key value pairs.

```json
{
    "actors": [
        {
            "age": 24,
            "gender": "f",
            "id": 1,
            "movie_id": 1,
            "name": "actor2"
        }
    ],
    "success": true
}
```
`POST /movies'`
* This requires permissions `post:movies`
* This endpoint helps user to create a new movies.
* Fields: movie title, release date.
* Returns: Success values
Example: curl http://127.0.0.1:5000/movies -X POST -H "Content-Type: application/json" -d '{"title":"new movie","release_date":"24-APR"}'

```json
{
    "success": true
}
```
Response if permission is not found:
```json
{
    "error": 403,
    "message": "Permission not found.",
    "success": false
}
```

`POST /actors'`
* This requires permissions `post:actors`
* This endpoint helps user to create a new actors.
* Fields: actors name, age, gender, movie_id.
* Returns: Success values
Example: curl http://127.0.0.1:5000/actors -X POST -H "Content-Type: application/json" -d '{"name":"new actor","age":24,"gender":"f","movie_id":1}'

```json
{
    "success": true
}
```
Response if permission is not found:
```json
{
    "error": 403,
    "message": "Permission not found.",
    "success": false
}
```

`DELETE '/movies/<movie_id>'`
* This endpoint helps user to delete movies based on the movie id.
* Fields: movie_id
* Returns success on deletion of the record.
* Returns 200 as request code if successful, else 404 if the id is not found
Example: curl -X DELETE http://127.0.0.1:5000/movies/2

```json
{
    "deleted": 2,
    "success": true
}
```
* Response body for not found record
```json
{
  "error":404,
  "message":"Data not found",
  "success":false
  }
```
Response if permission is not found:
```json
{
    "error": 403,
    "message": "Permission not found.",
    "success": false
}
```

`DELETE '/actors/<actor_id>'`
* This endpoint helps user to delete actors based on the actor id.
* Fields: actor_id
* Returns success on deletion of the record.
* Returns 200 as request code if successful, else 404 if the id is not found
Example: curl -X DELETE http://127.0.0.1:5000/actor/2

```json
{
    "deleted": 2,
    "success": true
}
```
* Response body for not found record
```json
{
  "error":404,
  "message":"Data not found",
  "success":false
  }
```
Response if permission is not found:
```json
{
    "error": 403,
    "message": "Permission not found.",
    "success": false
}
```

Error Handlers:

* Erros are handeled and gives a exact response to the user 
200: On successful operation
422: When operation is not proccesseble
404: When the resouce is not found

```json
{
  "error":404,
  "message":"Data not found",
  "success":false
}
```
RBAC failures:
Response if permission is not found:
```json
{
    "error": 403,
    "message": "Permission not found.",
    "success": false
}
```
