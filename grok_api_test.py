"""
Tests for the grok_api module
"""

import unittest
from unittest.mock import patch, MagicMock
from requests.exceptions import HTTPError
import grok_api

class TestGrokAPI(unittest.TestCase):
    """Test cases for grok_api module"""
    
    @patch('requests.post')
    @patch('grok_api.get_api_key')
    def test_grok_live_response_success(self, mock_get_api_key, mock_post):
        """Test successful API call with valid payload"""
        # Setup mocks
        mock_get_api_key.return_value = "test_api_key"
        mock_response = MagicMock()
        mock_response.json.return_value = {"choices": [{"message": {"content": "Test response"}}]}
        mock_post.return_value = mock_response
        
        # Test payload
        payload = {"messages": [{"role": "user", "content": "Hello"}]}
        
        # Call function
        result = grok_api.grok_live_response(payload)
        
        # Verify API was called with correct arguments
        mock_post.assert_called_once()
        call_args = mock_post.call_args[1]
        self.assertEqual(call_args["json"]["model"], grok_api.GROK_MODEL)
        self.assertEqual(call_args["json"]["messages"][0]["content"], "Hello")
        
        # Verify result
        self.assertEqual(result, {"choices": [{"message": {"content": "Test response"}}]})
    
    def test_invalid_payload(self):
        """Test that function raises error with invalid payload"""
        # Test with empty messages
        with self.assertRaises(ValueError):
            grok_api.grok_live_response({"messages": []})
        
        # Test with missing messages
        with self.assertRaises(ValueError):
            grok_api.grok_live_response({})
    
    @patch('requests.post')
    @patch('grok_api.get_api_key')
    def test_http_error_handling(self, mock_get_api_key, mock_post):
        """Test handling of HTTP errors from the API"""
        mock_get_api_key.return_value = "test_api_key"
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = HTTPError("500 Server Error")
        mock_post.return_value = mock_response
        
        with self.assertRaises(HTTPError):
            grok_api.grok_live_response({"messages": [{"role": "user", "content": "Hello"}]})
    
    @patch('grok_api.get_api_key')
    def test_api_key_failure(self, mock_get_api_key):
        """Test handling when API key retrieval fails"""
        mock_get_api_key.side_effect = ValueError("API key not found")
        
        with self.assertRaises(ValueError) as context:
            grok_api.grok_live_response({"messages": [{"role": "user", "content": "Hello"}]})
        self.assertEqual(str(context.exception), "API key not found")
    
    @patch('requests.post')
    @patch('grok_api.get_api_key')
    def test_invalid_json_response(self, mock_get_api_key, mock_post):
        """Test handling of non-JSON responses"""
        mock_get_api_key.return_value = "test_api_key"
        mock_response = MagicMock()
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_post.return_value = mock_response
        
        with self.assertRaises(ValueError):
            grok_api.grok_live_response({"messages": [{"role": "user", "content": "Hello"}]})
    
    @patch('requests.post')
    @patch('grok_api.get_api_key')
    def test_different_http_errors(self, mock_get_api_key, mock_post):
        """Test handling of different HTTP error status codes"""
        mock_get_api_key.return_value = "test_api_key"
        
        # Test 400 Bad Request
        mock_response_400 = MagicMock()
        mock_response_400.raise_for_status.side_effect = HTTPError("400 Bad Request")
        mock_post.return_value = mock_response_400
        
        with self.assertRaises(HTTPError):
            grok_api.grok_live_response({"messages": [{"role": "user", "content": "Bad request"}]})
        
        # Test 401 Unauthorized
        mock_response_401 = MagicMock()
        mock_response_401.raise_for_status.side_effect = HTTPError("401 Unauthorized")
        mock_post.return_value = mock_response_401
        
        with self.assertRaises(HTTPError):
            grok_api.grok_live_response({"messages": [{"role": "user", "content": "Unauthorized"}]})

if __name__ == "__main__":
    unittest.main()
