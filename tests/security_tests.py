import pytest
import requests

from ApiRequests.api_requests import ApiRequests
from data.expected_results import ExpectedResults
from data.globals import ApiHttpConstants


class TestsBookAPI(ApiRequests):
    """Security Tests for the book API endpoints."""
    @pytest.mark.xfail
    def test_unauthorized_access(self):
        """Test accessing endpoints without proper authorization."""
        # Assuming the API requires an authorization header
        response = self.get(f"/books")
        assert response.status_code == ApiHttpConstants.UNAUTHORIZED, \
            "Unauthorized access did not return 401."

    def test_invalid_input(self):
        """Test handling of invalid input data."""
        invalid_book_data = {"title": "", "author": ""}
        response = self.post("/books", json=invalid_book_data)
        assert response.status_code == ApiHttpConstants.BAD_REQUEST, \
            "Invalid input did not return 400."

    @pytest.mark.xfail
    def test_sql_injection(self):
        """Test for SQL injection vulnerability."""
        malicious_input = "' OR '1'='1"
        response = self.get(f"/books?title={malicious_input}")
        assert response.status_code == ApiHttpConstants.BAD_REQUEST, \
            "SQL injection attempt did not return 400."

    @pytest.mark.xfail
    def test_xss_attack(self):
        """Test for XSS vulnerability."""
        xss_payload = "<script>alert('XSS')</script>"
        response = self.post("/books", json={"title": xss_payload, "author": "Hacker"})
        assert response.status_code == ApiHttpConstants.BAD_REQUEST, \
            "XSS attempt did not return 400."