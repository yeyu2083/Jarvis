import unittest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from jarvis import speak, greet_user, take_user_input, USERNAME, BOTNAME

class TestJarvis(unittest.TestCase):
    
    @patch('pyttsx3.init')
    def test_speak(self, mock_init):
        # Setup mock
        mock_engine = MagicMock()
        mock_init.return_value = mock_engine
        
        # Test speak function
        test_text = "Hello test"
        speak(test_text)
        
        # Verify engine.say was called with correct text
        mock_engine.say.assert_called_once_with(test_text)
        # Verify runAndWait was called
        mock_engine.runAndWait.assert_called_once()

    @patch('jarvis.speak')
    @patch('jarvis.datetime')
    def test_greet_user_morning(self, mock_datetime, mock_speak):
        # Setup morning time
        mock_datetime.now.return_value = MagicMock(hour=8)
        
        # Call function
        greet_user()
        
        # Verify correct greeting was spoken
        mock_speak.assert_any_call(f"Buenos Dias {USERNAME}")
        mock_speak.assert_any_call(f"Yo soy {BOTNAME}. ¿Cómo puedo ayudarle?")

    @patch('speech_recognition.Recognizer')
    @patch('speech_recognition.Microphone')
    def test_take_user_input_normal(self, mock_microphone, mock_recognizer):
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

    @patch('speech_recognition.Recognizer')
    @patch('speech_recognition.Microphone')
    def test_take_user_input_exception(self, mock_microphone, mock_recognizer):
        # Setup mocks for exception case
        recognizer_instance = MagicMock()
        mock_recognizer.return_value = recognizer_instance
        recognizer_instance.recognize_google.side_effect = Exception()
        
        mock_microphone.return_value.__enter__.return_value = "mock_source"
        recognizer_instance.listen.return_value = "mock_audio"
        
        # Test function
        result = take_user_input()
        
        # Verify result when exception occurs
        self.assertEqual(result, 'None')

if __name__ == '__main__':
    unittest.main()