# apinote
A simple API backend that allows users to create,
read, update and delete notes. It should include a login system and the ability to
save notes to a remote database.

## Documentation
Below are the various request one can make to <code>https://apinote.onrender.com</code>, using [cURL](https://curl.se/docs/manpage.html), [Postman](https://www.postman.com/downloads/) or any other API tool.
- Adopted from: https://stubby4j.com/docs/admin_portal.html
- Inspired by Swagger API docs style & structure: https://petstore.swagger.io/#/pet

------------------------------------------------------------------------------------------

### Testing status

<details>
 <summary><code>GET</code> <code><b>/</b></code> <code>(Returns welcome message and documentation link)</code></summary>

##### Parameters

> None


##### Responses

> | http code | content-type              | response                                                                                                                 |
> |-----------|---------------------------|--------------------------------------------------------------------------------------------------------------------------|
> | `201`     | `application/json`        | `{"message": "Welcome to apinote!", "documentation": "https://github.com/josephtam-github/apinote/blob/main/README.md"}` |
> | `500`     | `text/html;charset=utf-8` | `Internal Server Error`                                                                                                  |

##### Example cURL

> ```bash
>  curl  -X GET -H "Accept: application/json" https://apinote.onrender.com
> ```

##### Example Postman
![Postman default example](/static/apinote-empty-get-request.png)

</details>

------------------------------------------------------------------------------------------

### Register user

<details>
 <summary><code>POST</code> <code><b>/register</b></code> <code>(Registers user to MySQL database and returns message</code></summary>

##### Parameters

> | name                      | type       | data type       | description                                                                                                                       |
> |---------------------------|------------|-----------------|-----------------------------------------------------------------------------------------------------------------------------------|
> | `username` and `password` | `required` | `object (JSON)` | The username and password which will be stored in MySQL database. <br> format: `{"name": "<USERNAME>", "password": "<PASSWORD>"}` |


##### Responses

> | http code     | content-type                      | response                                                            |
> |---------------|-----------------------------------|---------------------------------------------------------------------|
> | `201`         | `application/json`                | `{'message': 'registered successfully'}`                            |
> | `400`         | `application/json`                | `{"code":"400","message":"Bad Request"}`                            |
> | `405`         | `text/html;charset=utf-8`         | None                                                                |

##### Example cURL

> ```bash
>  curl https://apinote.onrender.com/register
>    -X POST
>    -H "Content-Type: application/json"
>    -d '{"name": "<USERNAME>", "password": "<PASSWORD>"}'
> ```

##### Example Postman
![Postman registration example](/static/apinote-register-post-request-2.png)

</details>

------------------------------------------------------------------------------------------

### Login user

<details>
 <summary><code>POST</code> <code><b>/login</b></code> <code>(Logs in user with Basic Auth and generates token key)</code></summary>

##### Parameters

> | name                      | type       | data type       | description                                                                                                            |
> |---------------------------|------------|-----------------|------------------------------------------------------------------------------------------------------------------------|
> | `username` and `password` | `required` | `object (JSON)` | The username and password which will be used to login. <br> format: `{"name": "<USERNAME>", "password": "<PASSWORD>"}` |


##### Responses

> | http code     | content-type                     | response                                 |
> |---------------|-----------------------------------|------------------------------------------|
> | `201`         | `application/json`               | `{'token': '<RANDOM_GENERATED_TOKEN>'}`  |
> | `400`         | `application/json`               | `{"code":"400","message":"Bad Request"}` |
> | `401`         | `application/json`               | `verification failed`                    |  

##### Example cURL

> ```bash
> $ curl --user <USERNAME>:<PASSWORD> https://apinote.onrender.com/login \
>    -X POST \
>    -H "Content-Type: application/json" \
>    -d '{"name": "<USERNAME>", "password": "<PASSWORD>"}'
> ```

##### Example Postman
![Postman login example](/static/apinote-login-post-request-2.png)

</details>

------------------------------------------------------------------------------------------

### Create a note

<details>
 <summary><code>POST</code> <code><b>/create</b></code> <code>(Create notes only accessible to logged in user)</code></summary>

##### Parameters

> | name                  | type       | data type       | description                                                                                                                                 |
> |-----------------------|------------|-----------------|---------------------------------------------------------------------------------------------------------------------------------------------|
> | `x-access-tokens`       | `required` | `Header`        | HTTP Request Header containing the token generated from`/login` i.e `<RANDOM_GENERATED_TOKEN>`                                            |
> | `title` and `content` | `required` | `object (JSON)` | The title and content of the note which will be stored in MySQL database. <br> format: `{"title": "<HEADING>", "content": "<NOTE_BODY>"}`   |


##### Responses

> | http code     | content-type                      | response                                                                                                                                     |
> |---------------|-----------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|
> | `201`         | `application/json`                | Returns the note created <br> format: `{"title": "<HEADING>", "content": "<NOTE_BODY>"}`                                                     |
> | `400`         | `application/json`                | `{"code":"400","message":"Bad Request"}`                                                                                                     |
> | `400`         | `application/json`                | Prompt to login: `{'message': 'a valid token is missing'}`                                                                                   |  
> | `400`         | `application/json`                | Specific detail: `{"message": "Something is wrong either an error has occurred or your token is invalid', "more detail": <SPECIFIC_DETAIL>}` |  

##### Example cURL

> ```bash
> $ curl -H "Authorization: Basic <RANDOM_GENERATED_TOKEN>" https://apinote.onrender.com/create   \
>    -X POST  \
>    -H "Content-Type: application/json"  \
>    -d '{"title": "<HEADER>", "content": "<BODY>"}'
> ```

##### Example Postman
Setting the `x-access-tokens` Header

![Postman create example](/static/apinote-token-header.png)

Sending two different note data

![Postman create example](/static/apinote-create-post-request-2.png)

![Postman create example](/static/apinote-create-post-request-4.png)

</details>

------------------------------------------------------------------------------------------

### List notes

<details>
 <summary><code>GET</code>or<code>POST</code> <code><b>/list</b></code> <code>(Returns a list of all notes created, along with their id and timestamp)</code></summary>

##### Parameters

> | name                  | type       | data type      | description                                                                                      |
> |-----------------------|------------|-----------------|-------------------------------------------------------------------------------------------------|
> | `x-access-tokens `      | `required` | `Header`       | HTTP Request Header containing the token generated from`/login` i.e `<RANDOM_GENERATED_TOKEN>` |


##### Responses

> | http code     | content-type                      | response                                                                                                                                     |
> |---------------|-----------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|
> | `201`         | `application/json`                | A list called `list_of_notes` containing an array of object of all notes created by user.                                                    |
> | `400`         | `application/json`                | `{"code":"400","message":"Bad Request"}`                                                                                                     |
> | `400`         | `application/json`                | Prompt to login: `{'message': 'a valid token is missing'}`                                                                                   |  
> | `400`         | `application/json`                | Specific detail: `{"message": "Something is wrong either an error has occurred or your token is invalid', "more detail": <SPECIFIC_DETAIL>}` |  

##### Example cURL

> ```bash
> $ curl -H "Authorization: Basic <RANDOM_GENERATED_TOKEN>" https://apinote.onrender.com/list   \
>    -X GET
> ```

##### Example Postman
Setting the `x-access-tokens` Header

![Postman create example](/static/apinote-token-header.png)

Sending list request

![Postman create example](/static/apinote-listnote-request.png)

</details>

------------------------------------------------------------------------------------------

### Read a note

<details>
 <summary><code>GET</code>or<code>POST</code> <code><b>/note/&lt;id&gt;</b></code> <code>(Returns a logged in user's note by using the note's id)</code></summary>

##### Parameters

> | name              | type       | data type       | description                                                                                    |
> |-------------------|------------|-----------------|------------------------------------------------------------------------------------------------|
> | `x-access-tokens` | `required` | `Header`        | HTTP Request Header containing the token generated from`/login` i.e `<RANDOM_GENERATED_TOKEN>` |
> | `id`              | `required` | `Header`        | Note id gotten from `/list`                                                                    |

##### Responses

> | http code     | content-type                      | response                                                                                                                                     |
> |---------------|-----------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|
> | `201`         | `application/json`                | Returns the note with particular id <br> format: `{"title": "<HEADING>", "content": "<NOTE_BODY>"}`                                          |
> | `400`         | `application/json`                | `{"code":"400","message":"Bad Request"}`                                                                                                     |
> | `400`         | `application/json`                | Prompt to login: `{'message': 'a valid token is missing'}`                                                                                   |  
> | `400`         | `application/json`                | Specific detail: `{"message": "Something is wrong either an error has occurred or your token is invalid', "more detail": <SPECIFIC_DETAIL>}` |  

##### Example cURL

> ```bash
> $ curl -H "Authorization: Basic <RANDOM_GENERATED_TOKEN>" https://apinote.onrender.com/note/<id>   \
>    -X GET
> ```

##### Example Postman
Setting the `x-access-tokens` Header

![Postman create example](/static/apinote-token-header.png)

Sending read request

![Postman create example](/static/apinote-getnote-post-request.png)

</details>

-----------------------------------------------------------------------------------------

### Update a note

<details>
 <summary><code>PATCH</code> <code><b>/note/&lt;id&gt;</b></code> <code>(Updates a logged in user's note by using the note's id)</code></summary>

##### Parameters

> | name              | type       | data type       | description                                                                                    |
> |-------------------|------------|-----------------|------------------------------------------------------------------------------------------------|
> | `x-access-tokens` | `required` | `Header`        | HTTP Request Header containing the token generated from`/login` i.e `<RANDOM_GENERATED_TOKEN>` |
> | `id`              | `required` | `Header`        | Note id gotten from `/list`                                                                    |

##### Responses

> | http code     | content-type                      | response                                                                                                                                     |
> |---------------|-----------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|
> | `201`         | `application/json`                | Returns the updated note with particular id <br> format: `{"title": "<HEADING>", "content": "<NOTE_BODY>"}`                                  |
> | `400`         | `application/json`                | `{"code":"400","message":"Bad Request"}`                                                                                                     |
> | `400`         | `application/json`                | Prompt to login: `{'message': 'a valid token is missing'}`                                                                                   |  
> | `400`         | `application/json`                | Specific detail: `{"message": "Something is wrong either an error has occurred or your token is invalid', "more detail": <SPECIFIC_DETAIL>}` |  

##### Example cURL

> ```bash
> $ curl -H "Authorization: Basic <RANDOM_GENERATED_TOKEN>" https://apinote.onrender.com/note/<id>   \
>    -X PATCH  \
>    -H "Content-Type: application/json"  \
>    -d '{"title": "<HEADER>", "content": "<BODY>"}'
> ```

##### Example Postman
Setting the `x-access-tokens` Header

![Postman create example](/static/apinote-token-header.png)

Sending update data

![Postman create example](/static/apinote-updatenote-post-request.png)

</details>

------------------------------------------------------------------------------------------

### Delete a note

<details>
 <summary><code>DELETE</code> <code><b>/note/&lt;id&gt;</b></code> <code>(Deletes a logged in user's note by using the note's id)</code></summary>

##### Parameters

> | name              | type       | data type       | description                                                                                    |
> |-------------------|------------|-----------------|------------------------------------------------------------------------------------------------|
> | `x-access-tokens` | `required` | `Header`        | HTTP Request Header containing the token generated from`/login` i.e `<RANDOM_GENERATED_TOKEN>` |
> | `id`              | `required` | `Header`        | Note id gotten from `/list`                                                                    |

##### Responses

> | http code     | content-type                      | response                                                                                                                                     |
> |---------------|-----------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|
> | `201`         | `text/html;charset=utf-8`         | Returns `note successfuly deleted`                                                                                                           |
> | `400`         | `application/json`                | `{"code":"400","message":"Bad Request"}`                                                                                                     |
> | `400`         | `application/json`                | Prompt to login: `{'message': 'a valid token is missing'}`                                                                                   |  
> | `400`         | `application/json`                | Specific detail: `{"message": "Something is wrong either an error has occurred or your token is invalid', "more detail": <SPECIFIC_DETAIL>}` |  

##### Example cURL

> ```bash
> $ curl -H "Authorization: Basic <RANDOM_GENERATED_TOKEN>" https://apinote.onrender.com/note/<id>   \
>    -X DELETE
> ```

##### Example Postman
Setting the `x-access-tokens` Header

![Postman create example](/static/apinote-token-header.png)

Sending delete request

![Postman create example](/static/apinote-delete-post-request-2.png)

</details>

------------------------------------------------------------------------------------------

## Tools used:
* [Python 3](https://www.python.org/download/releases/3.0/) - The language programming used
* [Flask](http://flask.pocoo.org/) - The web framework used
* [Flask Migrate](https://pypi.org/project/Flask-Migrate/) - The database migration
* [Virtualenv](https://virtualenv.pypa.io/en/latest/) - The virtual environment used
* [SQL Alchemy](https://www.sqlalchemy.org/) - The database library
* [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.3/) - Flask and SQL Alchemy connector
* [flask-marshmallow](https://flask-marshmallow.readthedocs.io/) - Integration layer for Flask and marshmallow (an object serialization/deserialization library)
* [PyJWT](https://pyjwt.readthedocs.io/) - Python library which allows you to encode and decode JSON Web Tokens

## Clone or Download

You can clone or download this project
```
> Clone : git clone https://github.com/josephtam-github/apinote.git
```

## Authors

* **Joseph Tam Ogbo** - [LinkedIn](https://www.linkedin.com/in/joseph-tam-b9700b1a6) [Twitter](https://www.twitter.com/Joseph_tam_)

