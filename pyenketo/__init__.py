import requests
import json
from urlparse import urljoin


class EnketoException(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message


class Http400(EnketoException):
    code = 400
    message = "bad request"


class Http401(EnketoException):
    code = 401
    message = "Access denied: invalid authentication token."


class Http403(EnketoException):
    code = 403
    message = "Authentication succeeded but account inactive or quota filled" \
              " up."


class Http404(EnketoException):
    code = 404
    message = "Resource was not found in the database"


class Http405(EnketoException):
    code = 405
    message = "Request not allowed"


class Http410(EnketoException):
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


class Enketo(object):
    ENKETO_URL = 'https://enketo.org'
    API_PATH = '/api_v1'
    SURVEY_PATH = '/survey'
    INSTANCE_PATH = '/instance'
    API_TOKEN = None

    def configure(self, ENKETO_URL, API_TOKEN):
        self.ENKETO_URL = ENKETO_URL
        self.API_TOKEN = API_TOKEN

    def get_survey_url(self, server_url, form_id):
        payload = {'server_url': server_url, 'form_id': form_id}
        response = requests.get(
            urljoin(
                self.ENKETO_URL,
                "{}{}".format(self.API_PATH, self.SURVEY_PATH)),
            auth=(self.API_TOKEN, ''),
            params=payload)
        content = json.loads(response.content)
        if response.status_code != 200:
            raise exception_for_response_code(response.status_code)(
                response.status_code, content['message'])
        else:
            return content['url']

    def get_edit_url(
            self, server_url, form_id, xml_instance, instance_id, return_url):
        payload = {
            'server_url': server_url,
            'form_id': form_id,
            'instance': xml_instance,
            'instance_id': instance_id,
            'return_url': return_url
        }
        response = requests.post(
            urljoin(
                self.ENKETO_URL,
                "{}{}".format(self.API_PATH, self.INSTANCE_PATH)),
            auth=(self.API_TOKEN, ''),
            data=payload)
        content = json.loads(response.content)
        if response.status_code != 201:
            raise exception_for_response_code(response.status_code)(
                response.status_code, content['message'])
        else:
            return content['edit_url']