class AuthMiddleware(object):

    def process_request(self, req, resp):
        token = req.get_header('X-Auth-Token')
        project = req.get_header('X-Project-ID')

        if token is None:
            description = ('Please provide an auth token '
                           'as part of the request.')

            raise falcon.HTTPUnauthorized('Auth token required',
                                          description,
                                          href='http://docs.example.com/auth')

        if not self._token_is_valid(token, project):
            description = ('The provided auth token is not valid. '
                           'Please request a new token and try again.')

            raise falcon.HTTPUnauthorized('Authentication required',
                                          description,
                                          href='http://docs.example.com/auth',
                                          scheme='Token; UUID')

    def _token_is_valid(self, token, project):
        return True  # Suuuuuure it's valid...
