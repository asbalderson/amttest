"""Test the error modules."""

import json

from .base_test import BaseTest

from ..errors import apierror, forbidden, gone, internalservererror, \
    methodnotallowed, notfound, unauthorized


class ErrorTest(BaseTest):
    """Test all the error objects in the API."""

    def create_app(self):
        """Configure and stand up the flask app for testing """
        return BaseTest.create_app(self)

    def setUp(self):
        """Create a database for testing."""
        BaseTest.setUp(self)

    def tearDown(self):
        """Delete the database used during testing."""
        BaseTest.tearDown(self)

    # pylint: disable=E1101
    def test_api_error(self):
        """Test the creation of an api error"""
        message = 'abc123'
        api_error = apierror.APIError(message)
        self.assertIsInstance(api_error, Exception,
                              'Api erorr should be an Exception.')
        self.assertEqual(message, api_error.message)

        with_kwarg = apierror.APIError(message, thing='thing')
        self.assertEqual('thing', with_kwarg.thing)
        result_dict = {'message': 'abc123',
                       'thing': 'thing'}
        for k, val in result_dict.items():
            self.assertEqual(val, with_kwarg.to_json().json[k],
                             'set value %s is not in the object json' % k)

    def test_forbidden(self):
        """Test the forbidden error."""
        message = 'this is an error'
        err = forbidden.Forbidden(message)
        self.assertIsInstance(err, apierror.APIError,
                              'forbidden should be an instance of APIError')
        self.assertEqual(err.code, 403,
                         'forbidden is a 403')
        self.assertEqual(err.error, 'Forbidden',
                         'the forbidden error should be "Forbidden"')
        forbidden_error = forbidden.handle_forbidden(err)
        print(forbidden_error.json)
        self.compare_object(forbidden_error.json, err.to_json().json)
        self.assertEqual(forbidden_error.status_code, err.code,
                         'the response should match the error code')

        message2 = 'forbidden2'
        abort403 = forbidden.handle_403(message2)

        self.assertEqual(message2, abort403.json['message'],
                         'abort 403 doesnt capture errors correctly')
        self.assertEqual(abort403.status_code, 403,
                         'abort 403 should have a 403 status code')

    def test_gone(self):
        """Test the gone error."""
        pass

    def test_internalservererror(self):
        """Test the internalservererror."""
        pass

    def test_methodnotallowed(self):
        """Test the methodnotallowed error."""
        pass

    def test_notfound(self):
        """Test the not found error."""
        pass

    def test_unauthorized(self):
        """Test the unauthorized error."""
        pass
