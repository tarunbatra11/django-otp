# django-otp

This library help developers to autheticate users using their phone with otp. This is exactly same as whatsapp authentication and not two-factor authentication.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

```
pip3 install django
pip3 install django-oauth-toolkit
```

### Installing

Change database configuration. If you are using mysql then create database with name "otp". Install prerequisites and clone the library. Move inside project directory.

```
./manage.py makemigrations
./manage.py migrate
./manage.py createsuperuser
```
This will create database and super user.

## Deployment

To run django server on local machine

```
./manage.py runserver 0.0.0.0:8080
```
Now, you can make calls on localhost:8080. To deploy on live use proper web server(nginx or apache)

## Flow

Login and create client application to get client id, client secret.

```
localhost:8080/admin/
localhost:8080/o/application/
```
Choose confidential and Resource owner password protected. Once client is created go to database and update authorization_grant_type to otp in oauth2_provider_application table.

### Call flow

* Client will make request with phone number and server will send SMS with code on that phone number.
* Client will make request verify code, this call will have code generated and and phone number, as response client will get a random string.
* Client will make request to create the user, for this call there has to be 3 additional keys - account(nested field) with phone number, secret-identifier(in response of previous call) and auto_username=true.
* Once user is created client can send another call to get access token with grant_type as otp.

### Calls

```
curl -X POST -d "phone=1234567822" "http://localhost:8000/otp/getcode/"
curl -X POST -d "code=693474&phone=1234567822" "http://localhost:8000/otp/verifycode/"
curl -X PUT -H "Content-Type: application/json" -d '{"email":"tarunuser@gmail.com","first_name":"tarun","last_name":"batra", "password": "walkman123","account":{"blood_group":"b+","dob":"1989-12-12T00:00:00Z","phone":"7894561235","address":"vijetha midas touch","zip_code":"500081","verified":false}, "auto_username": true, "secret_identifier": "c1e1d13d51bb90dd3b9552a37a70cac6cc8fa9d8e8b0f812"}' http://localhost:8000/api/v1/user/
curl -X POST -d "grant_type=otp&phone=1234567895" -u"AEzSrN2kn2ONpDB56RD4kU2IRCvjrA19Tq2WGuzY:5JvN7Yg94m9w3czCzkg0RRNgdTP0DsWnueSjB7R5FUqSMwYJrcbyOxDxeSHu6fpT0W8m2OHv4WgT7Gm2y3KKrqaOwuv7xwaVyg9cDpz9MXrpPSVGXzTtND34rdzsFJ6L" http://localhost:8000/o/extended_token/
```
This will provide the access token with expiration time, refresh token to client for the user. Now client can make requests on behalf of user using access token. To send SMS on phone number you need to integrate with SMS provider.

## Built With

* [Django](https://www.djangoproject.com/) - The web framework used
* [Django oauth toolkit](https://django-oauth-toolkit.readthedocs.io/en/latest/install.html) - Oauth2 provider

## Contributing

Please read [CONTRIBUTING.md](https://www.github.com/tarunbatra11) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [git](https://github.com/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Tarun Batra** - *Initial work* - [tarunbatra11](https://github.com/tarunbatra11)

See also the list of [contributors](contributions.md) who participated in this project.

## License

This project can be used by anyone.
