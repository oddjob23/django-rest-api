import json

from rest_framework.renderers import JSONRenderer


class UserJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        # decode token if token is received as byte object
        # catch errors if any - data.get('errors')
        errors = data.get('errors', None)

        if errors is not None:
            # default JSONRenderer handle to render errors
            return super(UserJSONRenderer, self).render(data)

        # get token
        token = data.get('token', None)
        if token is not None and isinstance(token, bytes):
            data['token'] = token.decode('utf-8')

        # dump data into json format and return it
        return json.dumps({
            'user': data
        })
