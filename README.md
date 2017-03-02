# runkeeper-api

A simple python script to get data from Runkeeper's HealthGraph API

## Setup and obtain access token

1. Clone or fork this project.

2. The idea is to start a webserver and make a request to the API for an access token (the API requires a callback URL which can be locally hosted using the 'gettoken.html' provided and a simple python HTTP server such as:
```python
  python -m SimpleHTTPServer 8000
```

3. The REDIRECT_URL field should then be set to: 'http://localhost.com/gettoken.html

4. Next step is to make the request to the HealthGraph API by accessing this link replacing the [REDIRECT_URL] with the one you setup (replacing '/' with '%2F') and replaing [CLIENT_ID] with your client ID:
https://runkeeper.com/apps/authorize?response_type=code&client_id=[MY_CLIENT_ID]&redirect_uri=http%3A%2F%2F[MY_URL.COM]

5. Your redirect URL will then be opened and the field 'code' will be in the URL and should be pasted into the 'code' form field together with your credentials. The access token is now just a 'submit' away.

6. Copy the access token into the ACCESS_TOKEN field in your program

7. Run 'requirements.sh' to create a virtualenv for your project and install the relevant libraries using pip (NOT as root)

## First use example

1. Replace values in 'credentials.py' with your personal ones

2. Add these lines in your python script:
```python
  import runkeeper
  import credentials
```

3. Create runkeeper-api instance and download all of your data into two separate .csv files, one with a row per activity with general information and another one with all the datapoints identified by the activity ID:
```python
  rk = RunKeeper(credentials.CLIENT_ID, credentials.CLIENT_SECRET, credentials.ACCESS_TOKEN)
  rk.get_all_activities_csv()
```

## Current state

Right now the script downloads all of the user's activities and can store them in a .csv file.

Suggestions and help with improvements are welcomed! Some more info on the types of data that can be obtained via the healthgraph API:
https://runkeeper.com/developer/healthgraph/example-api-calls
