import unittest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

# Importar después de ajustar el path
from jarvis import speak, greet_user, take_user_input, USERNAME, BOTNAME

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

if __name__ == '__main__':
    unittest.main()