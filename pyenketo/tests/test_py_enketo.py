import unittest
import base64

from httmock import urlmatch, HTTMock
from pyenketo import PyEnketo, Http404


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

2
@urlmatch(netloc=r'(.*\.)?test.enketo\.org$', path='/api_v1/survey')
def get_survey_mock(url, request):
    # if the token is not valid, return a 401
    token_valid, response = check_token(request)
    if not token_valid:
        return response

    return '{"code": "200", "url": "https://cz2pj.enketo.org/webform"}'


class TestPyENketo(unittest.TestCase):
    def test_get_survey_url(self):
        py_enketo = PyEnketo()
        py_enketo.configure(
            ENKETO_API_URL='https://test.enketo.org/')

        with HTTMock(get_survey_mock):
            url = py_enketo.get_survey_url(
                'https://testserver.com/bob', 'widgets')
            self.assertEqual(url, "https://cz2pj.enketo.org/webform")

    def test_get_survey_notexist(self):
        py_enketo = PyEnketo()
        py_enketo.configure(
            ENKETO_API_URL='https://enketo.org/')
        with HTTMock(get_survey_mock):
            self.assertRaises(
                Http404,
                py_enketo.get_survey_url,
                'https://testserver.com/notexist',
                'widgets')



