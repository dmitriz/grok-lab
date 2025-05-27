"""
Tests for the grok_api module
"""

import unittest
from unittest.mock import patch, MagicMock
import grok_api
import json
from requests.exceptions import RequestException, HTTPError, JSONDecodeError

class TestGrokAPI(unittest.TestCase):
  """Test cases for grok_api module"""
  
  @patch('requests.post')
  @patch('grok_api.get_api_key')
  def test_api_key_retrieval_failure(self, mock_get_api_key, mock_post):
    """Test that function properly handles API key retrieval failure"""
    # Setup mock to raise ValueError
    mock_get_api_key.side_effect = ValueError("API key not found")
    class TestGrokAPI(unittest.TestCase):
      """Test cases for grok_api module"""
      
    # 
      @patch('requests.post')
      @patch('grok_api.get_api_key')
      def test_api_key_retrieval_failure(self, mock_get_api_key, mock_post):
        """Test that function properly handles API key retrieval failure"""
        # Setup mock to raise ValueError
        mock_get_api_key.side_effect = ValueError("API key not found")
        
        # Create test payload
        payload = {"messages": [{"role": "user", "content": "Hello"}]}
        
        # Verify that the ValueError is propagated
        with self.assertRaises(ValueError) as context:
          grok_api.grok_live_response(payload)
        
        # Verify the error message
        self.assertEqual(str(context.exception), "API key not found")
        
        # Verify that requests.post was never called
        mock_post.assert_not_called()
      
      @patch('requests.post')
      @patch('grok_api.get_api_key')
      def test_grok_live_response_success(self, mock_get_api_key, mock_post):
        """Test successful API call with valid payload"""
        # Setup mocks
        mock_get_api_key.return_value = "test_api_key"
        mock_response = MagicMock()
        mock_response.json.return_value = {"choices": [{"message": {"content": "Test response"}}]}
        mock_post.return_value = mock_response
        
        # Create test payload
        payload = {"messages": [{"role": "user", "content": "Hello"}]}
        
        # Call function
        result = grok_api.grok_live_response(payload)
        
        # Verify API call was made correctly
        mock_post.assert_called_once()
        call_kwargs = mock_post.call_args[1]
        sent_payload = call_kwargs["json"]
        
        # Verify payload modifications
        self.assertEqual(sent_payload["search_parameters"]["mode"], "on")
        self.assertEqual(sent_payload["model"], grok_api.GROK_MODEL)
        self.assertEqual(sent_payload["messages"][0]["content"], "Hello")
        
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
      def test_grok_live_response_invalid_json(self, mock_get_api_key, mock_post):
        """Test API call where response body is invalid JSON"""
        mock_get_api_key.return_value = "test_api_key"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = json.JSONDecodeError("Expecting value", "", 0)
        mock_post.return_value = mock_response
        
        payload = {"messages": [{"role": "user", "content": "Hello"}]}
        
        # Expect the JSON decode error to be propagated
        with self.assertRaises(json.JSONDecodeError):
          grok_api.grok_live_response(payload)
      
      @patch('requests.post')
      @patch('grok_api.get_api_key')
      def test_http_error_handling(self, mock_get_api_key, mock_post):
        """Test handling of HTTP errors from the API"""
        mock_get_api_key.return_value = "test_api_key"
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = HTTPError("500 Server Error")
        mock_post.return_value = mock_response
        
        payload = {"messages": [{"role": "user", "content": "Hello"}]}
        
        # Expect the HTTP error to be propagated
        with self.assertRaises(HTTPError):
          grok_api.grok_live_response(payload)
      
      @patch('requests.post')
      @patch('grok_api.get_api_key')
      def test_request_exception_handling(self, mock_get_api_key, mock_post):
        """Test handling of general request exceptions"""
        mock_get_api_key.return_value = "test_api_key"
        mock_post.side_effect = RequestException("Connection error")
        
        payload = {"messages": [{"role": "user", "content": "Hello"}]}
        
        # Expect the request exception to be propagated
        with self.assertRaises(RequestException):
          grok_api.grok_live_response(payload)

    if __name__ == "__main__":
      unittest.main()Create test payload
    payload = {"messages": [{"role": "user", "content": "Hello"}]}
    
    # Verify that the ValueError is propagated
    with self.assertRaises(ValueError) as context:
      grok_api.grok_live_response(payload)
    
    # Verify the error message
    self.assertEqual(str(context.exception), "API key not found")
    
    # Verify that requests.post was never called
    mock_post.assert_not_called()
    """Test successful API call with valid payload"""
    # Setup mocks
    mock_get_api_key.return_value = "test_api_key"
    mock_response = MagicMock()
    mock_response.json.return_value = {"choices": [{"message": {"content": "Test response"}}]}
    mock_post.return_value = mock_response
    
    # Create test payload
    payload = {"messages": [{"role": "user", "content": "Hello"}]}
    
    # Call function
    result = grok_api.grok_live_response(payload)
    
    # Verify API call was made correctly
    mock_post.assert_called_once()
    call_kwargs = mock_post.call_args[1]
    sent_payload = call_kwargs["json"]
    
    # Verify payload modifications
    self.assertEqual(sent_payload["search_parameters"]["mode"], "on")
    self.assertEqual(sent_payload["model"], grok_api.GROK_MODEL)
    self.assertEqual(sent_payload["messages"][0]["content"], "Hello")
    
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

if __name__ == "__main__":
  unittest.main()
