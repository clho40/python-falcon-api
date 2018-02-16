# Python : Falcon RESTFul API - MongoEngine - MongoDB - PyTest - Waitress

To start API server,

1. Install the required dependencies from requirements.txt
```
pip install -r requirements.txt
```

2. Start MongoDB server. Update connection string in /src/models.py if needed
```Python
connect('configapi') # Modify this if needed. Refer to Falcon's documentation
```

3. Navigate to /src and start Waitress server (for Windows only)
```
cd src
waitress-serve --port=8000 app:app
```

4. Browse the URL using browser or Postman Chrome App

