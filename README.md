# Facebook helpers

## Requirements

You should have the facebook [python sdk](https://github.com/facebook/python-sdk) installed. After
that install the helpers and import as you need. The helper class is using CherryPy so you
will also need that installed.

## Usage

Create a new helper with your app id's:

    fb = FBHelper(APP_ID, APP_SECRET, BASE_URL)

You can find the id & secret within your app settings. The base url is where the
application is configured to be redirecting too. This must match what you've
supplied Facebook in the app settings. Further redirect_uri updates will be
based off of this base_url.

## Login method

Facebook has a 2 step login method. First, initialize a request. Facebook will
respond with a new *code* param in the URL. Check that is present and if so
you can authorize the application. At this stage pass in the permissions you
will need for your app:

    if code is None:
        fb.start_login(permissions='publish_checkins,publish_stream')
    else:
        access_token = fb.post_authorize(code)

Facebook should return with a valid access token. If the process fails to return
a valid access token the app will return *None* so check before using the token
with the graph calls.

## Issues

This is a "barely working" class to aid dev'ing locally. It doesn't cover edge
cases or handle errors beyond getting it working for now. Your mileage may vary.
