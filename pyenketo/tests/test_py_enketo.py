import uuid
import unittest
import base64
import urlparse

from httmock import urlmatch, HTTMock
from pyenketo import Enketo, Http404


def check_token(request):
    auth_type, value = tuple(request.headers['Authorization'].split(" "))
    token = base64.b64decode(value)
    if token != 'abc:':
        return False, {
            'status_code': 401,
            'content': '{"code": "401", "message": "Access denied: invalid'
                       ' authentication token."}'
        }
    else:
        return True, None


@urlmatch(netloc=r'(.*\.)?test.enketo\.org$', path='/api_v2/survey')
def get_survey_mock(url, request):
    # if the token is not valid, return a 401
    token_valid, response = check_token(request)
    if not token_valid:
        return response

    # check for non-existent survey
    server_url = urlparse.unquote(urlparse.urlparse(url.query).path)
    path = urlparse.urlparse(
        dict(urlparse.parse_qsl(server_url))['server_url']).path
    if path == '/notexist':
        return {
            'status_code': 404,
            'content': '{"message": "Form does not exist"}'
        }

    return '{"code": "200", "url": "https://cz2pj.enketo.org/webform"}'


@urlmatch(netloc=r'(.*\.)?test.enketo\.org$', path='/api_v2/instance')
def get_edit_url_mock(url, request):
    # if the token is not valid, return a 401
    token_valid, response = check_token(request)
    if not token_valid:
        return response

    return {
        'status_code': 201,
        'content': '{"code": "201", "edit_url": "https://cz2pj-0.enketo.org/webform/edit?instance_id=2"}'
    }


class TestPyEnketo(unittest.TestCase):
    def test_get_survey_url(self):
        enketo = Enketo()
        enketo.configure(
            ENKETO_URL='https://test.enketo.org/', API_TOKEN='abc')

        with HTTMock(get_survey_mock):
            url = enketo.get_survey_url(
                'https://testserver.com/bob', 'widgets')
            self.assertEqual(url, "https://cz2pj.enketo.org/webform")

    def test_get_survey_notexist(self):
        enketo = Enketo()
        enketo.configure(
            ENKETO_URL='https://test.enketo.org/', API_TOKEN='abc')
        with HTTMock(get_survey_mock):
            self.assertRaises(
                Http404,
                enketo.get_survey_url,
                'https://testserver.com/notexist',
                'widgets')

    def test_get_edit_url(self):
        enketo = Enketo()
        enketo.configure(
            ENKETO_URL='https://test.enketo.org/', API_TOKEN='abc')
        xml_instance = '<?xml version=\'1.0\' ?><clinic_registration id="clinic_registration"><formhub><uuid>73242968f5754dc49c38463af658f3d2</uuid></formhub><user_id>0</user_id><clinic_name>Test clinic</clinic_name><meta><instanceID>uuid:ec5ce15e-5a0a-4246-93fe-acf60ef69bf2</instanceID></meta></clinic_registration>'
        instance_id = uuid.uuid4()
        return_url = 'https://testserver.com/bob/1'
        with HTTMock(get_edit_url_mock):
            enketo.get_edit_url(
                'https://testserver.com/bob',
                'widgets',
                xml_instance,
                instance_id,
                return_url)
