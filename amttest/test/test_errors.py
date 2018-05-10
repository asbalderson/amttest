"""Test the error modules."""

from operator import attrgetter

from .base_test import BaseTest

from ..errors import apierror, forbbiden, gone, internalservererror, \
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
        pass

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
