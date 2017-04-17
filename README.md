# Quoterly
This is a repository for the series of articles about creating RESTful application with Flask.

## Introduction

The article can be found [in my blog](https://dubovyksergey.wordpress.com/2017/04/17/restful-application-with-python-flask-and-sqlite-part-1-basics/). In this article I`ll tell how to build a very basic Flask application which works as a back-end for the online quotes service. It will support database, authorization and will work via REST API.

## Deployment

To run this code on your local computer clone this repository, enter the directory with it and run the following commands in your shell
```
mkdir flaskrest
cd flaskrest
sudo apt-get install python3 python3-pip python3-venv
python3 -m venv flaskenv # create virtual environment
source flaskenv/bin/activate # and activate it
pip3 install flask # this also automatically installs sqlite
```
After that run start.py script, which will create a database file and the launch main.py, which is the main module of the Quoterly application.

## Contribution

There is a quite long list of imporevemnts to be done in this app to make it better:

* Add protection against SQL-injections
* Change RDBMS to MySQL instead of SQLite
* Add quotes rating
* Add multi-threading
* Add front-end (to be done in next article)
* Add password hashing (as saving them unencrypted in our database is too… strange)
* Add HTTPS support, so that passwords won’t be sent as open text

So, if you feel that you`ve got some time to improve this example application and help somebody in learning Python development, feel free to fork this repo, modify it and propose your pull requests.

## License

All the code in this repository is published under the MIT License.
