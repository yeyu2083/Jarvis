import unittest
from unittest.mock import patch, MagicMock, mock_open
import sys
from pathlib import Path
import tempfile
import os

sys.path.append(str(Path(__file__).parent.parent))

from jarvis import (
    speak, greet_user, take_user_input, 
    save_temp_file, detect_duplicate_content,
    USERNAME, BOTNAME
)

class TestJarvis(unittest.TestCase):
    
    @patch('jarvis.AUDIO_ENABLED', True)
    @patch('jarvis.engine')
    def test_speak_with_audio(self, mock_engine):
        # Test speak function when audio is enabled
        test_text = "Hello test"
        speak(test_text)
        
        # Verify engine.say was called with correct text
        mock_engine.say.assert_called_once_with(test_text)
        mock_engine.runAndWait.assert_called_once()
    
    @patch('jarvis.AUDIO_ENABLED', False)
    @patch('builtins.print')
    def test_speak_without_audio(self, mock_print):
        # Test speak function when audio is disabled
        test_text = "Hello test"
        speak(test_text)
        
        # Verify print was called with correct text
        mock_print.assert_called_once_with(f"{BOTNAME}: {test_text}")
    
    @patch('jarvis.speak')
    @patch('jarvis.datetime')
    def test_greet_user_morning(self, mock_datetime, mock_speak):
        # Setup morning time
        mock_datetime.datetime.now.return_value = MagicMock(hour=8)
        
        # Call function
        greet_user()
        
        # Verify correct greeting was spoken
        mock_speak.assert_any_call(f"Buenos Días {USERNAME}")
        mock_speak.assert_any_call(f"Yo soy {BOTNAME}. ¿Cómo puedo ayudarle?")
    
    @patch('jarvis.AUDIO_ENABLED', True)
    @patch('speech_recognition.Recognizer')
    @patch('speech_recognition.Microphone')
    def test_take_user_input_audio(self, mock_microphone, mock_recognizer):
        # Setup mocks
        recognizer_instance = MagicMock()
        mock_recognizer.return_value = recognizer_instance
        recognizer_instance.recognize_google.return_value = "hola jarvis"
        
        mock_microphone.return_value.__enter__.return_value = "mock_source"
        recognizer_instance.listen.return_value = "mock_audio"
        
        # Test function
        result = take_user_input()
        
        # Verify recognizer was called correctly
        recognizer_instance.recognize_google.assert_called_once_with(
            "mock_audio", 
            language='es-ES'
        )
        self.assertEqual(result, "hola jarvis")
    
    @patch('jarvis.AUDIO_ENABLED', False)
    @patch('builtins.input')
    def test_take_user_input_text(self, mock_input):
        # Setup mock for text input
        mock_input.return_value = "hola jarvis"
        
        # Test function
        result = take_user_input()
        
        # Verify result
        self.assertEqual(result, "hola jarvis")

    @patch('tempfile.NamedTemporaryFile')
    def test_save_temp_file(self, mock_temp):
        # Setup mock temp file
        mock_file = MagicMock()
        mock_file.name = '/tmp/jarvis_test.txt'
        mock_temp.return_value.__enter__.return_value = mock_file
        
        # Test saving content
        result = save_temp_file("Test content")
        
        # Verify temp file was created and written to
        self.assertEqual(result, '/tmp/jarvis_test.txt')
        mock_file.write.assert_called_once_with("Test content")

    @patch('pathlib.Path.rglob')
    @patch('builtins.open', new_callable=mock_open)
    def test_detect_duplicate_content_no_duplicates(self, mock_file, mock_rglob):
        # Setup mock files
        mock_rglob.return_value = [Path('file1.txt'), Path('file2.txt')]
        mock_file.return_value.__enter__.return_value.read.side_effect = [
            b'content1',
            b'content2'
        ]
        
        # Test duplicate detection
        result = detect_duplicate_content()
        
        # Verify no duplicates found
        self.assertEqual(result, {})

    @patch('pathlib.Path.rglob')
    @patch('builtins.open', new_callable=mock_open)
    def test_detect_duplicate_content_with_duplicates(self, mock_file, mock_rglob):
        # Setup mock files with duplicate content
        mock_rglob.return_value = [
            Path('file1.txt'),
            Path('file2.txt'),
            Path('file3.txt')
        ]
        mock_file.return_value.__enter__.return_value.read.side_effect = [
            b'duplicate content',
            b'duplicate content',
            b'unique content'
        ]
        
        # Test duplicate detection
        result = detect_duplicate_content()
        
        # Verify duplicates were found
        self.assertTrue(len(result) > 0)
        
        # Get the hash key for the duplicate content
        hash_key = list(result.keys())[0]
        
        # Verify the duplicate files are identified
        self.assertEqual(len(result[hash_key]), 2)
        self.assertIn('file1.txt', result[hash_key][0])
        self.assertIn('file2.txt', result[hash_key][1])

    def test_save_temp_file_error(self):
        with patch('tempfile.NamedTemporaryFile') as mock_temp:
            # Setup mock to raise an exception
            mock_temp.side_effect = Exception("Test error")
            
            # Test error handling
            result = save_temp_file("Test content")
            
            # Verify None is returned on error
            self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()