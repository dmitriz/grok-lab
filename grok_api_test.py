"""
Tests for the grok_api module
"""

import unittest
from unittest.mock import patch, MagicMock
import grok_api

class TestGrokAPI(unittest.TestCase):
  """Test cases for grok_api module"""
  
  @patch('requests.post')
  @patch('grok_api.get_api_key')
  def test_grok_live_response(self, mock_get_api_key, mock_post):
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
