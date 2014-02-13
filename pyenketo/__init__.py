import requests
import json
from urlparse import urljoin


class PyEnketoException(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message


class Http400(PyEnketoException):
    code = 400
    message = "bad request"


class Http401(PyEnketoException):
    code = 401
    message = "Access denied: invalid authentication token."


class Http403(PyEnketoException):
    code = 403
    message = "Authentication succeeded but account inactive or quota filled" \
              " up."


class Http404(PyEnketoException):
    code = 404
    message = "Resource was not found in the database"


class Http405(PyEnketoException):
    code = 405
    message = "Request not allowed"


class Http410(PyEnketoException):
    code = 410
    message = "Endpoint deprecated"


status_code_exception_mapping = {
    (400, Http400),
    (401, Http401),
    (403, Http403),
    (404, Http404),
    (405, Http405),
    (410, Http410)
}


def exception_for_response_code(status_code):
    excs = filter(
        lambda mapping: mapping[0] == status_code,
        status_code_exception_mapping)
    code, klass = excs[0]
    return klass


class PyEnketo(object):
    ENKETO_URL = 'https://enketo.org/api_v1'
    API_PATH = '/api_v1'
    SURVEY_PATH = '/survey'

    def configure(self, *args, **kwargs):
        self.__dict__.update(kwargs)

    def get_survey_url(self, server_url, form_id):
        payload = {'server_url': server_url, 'form_id': form_id}
        response = requests.get(
            urljoin(
                self.ENKETO_URL,
                "{}{}".format(self.API_PATH, self.SURVEY_PATH)),
            auth=('abc', ''),
            params=payload)
        content = json.loads(response.content)
        if response.status_code != 200:
            raise exception_for_response_code(response.status_code)(
                response.status_code, content['message'])
        else:
            return content['url']
