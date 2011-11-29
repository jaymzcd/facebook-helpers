import urllib
import urlparse
import cherrypy

class FBHelper(object):

    graph_base = 'https://graph.facebook.com/'

    def __init__(self, app_id, app_secret, app_url_base):
        """
            A simple wrapper around some FB graph and auth calls to ease
            development. Pass in your app secret, id & the base of the
            url you're working from and have put into app settings.
        """
        self.app_id = app_id
        self.app_secret = app_secret
        self.app_url = app_url_base+'%s'

    def start_login(self, redirect_path='/login/', permissions=None):
        """
            Starts a login via facebook for a given app - the flow involves
            the OAuth request sending back a verfication code, we then need to
            use that to actually complete the authorization and get a users
            access token.

            Permissions should be a comma seperated string of request perms. Eg

                offline_access,publish_checkins,publish_stream
        """

        # We need to just pass our app id and where to come back to
        args = dict(client_id=self.app_id, redirect_uri=self.app_url % redirect_path)
        if permissions:
            args.update(dict(scope=permissions))

        # Now redirect to facebook, they'll authenticate us and send us back
        raise cherrypy.HTTPRedirect(self.graph_base + 'oauth/authorize?'+urllib.urlencode(args))

    def post_authorize(self, code, redirect_path='/login/'):
        """
            Finish the authentication of a user - returns an access token that
            can be used assuming the user authorized the app completely.
        """

        # For authorizing the app fully we now need to send our secrets through
        # and the verfication code from the start_login step
        args = dict(client_id=self.app_id, client_secret=self.app_secret,
            redirect_uri=self.app_url % redirect_path, code=code)

        # Process response - if the user authorizes the app we'll have an access
        # token from this step. Return that or None
        auth_url = self.graph_base + 'oauth/access_token?' +urllib.urlencode(args)
        response = urllib.urlopen(auth_url).read()
        auth_components = urlparse.parse_qs(response)
        try:
            access_token = auth_components['access_token'][-1]
            return access_token
        except KeyError, IndexError:
            return None
