import pygame  # Handles audio playback
import random  # For random choices
import asyncio  # For async operations
import edge_tts  # For text-to-speech conversion
import os  # For file operations
from dotenv import load_dotenv  # For reading environment variables

# Load environment variables from the .env file
load_dotenv()

# Retrieve voice setting from .env
AssistantVoice = os.getenv("AssistantVoice", "en-US-JennyNeural")  # Default to Jenny Neural if missing

# Asynchronous function to convert text to an audio file
async def TextToAudioFile(text) -> None:
    file_path = "Data/speech.mp3"  # Save path for the speech file

    # Remove previous audio file if it exists
    if os.path.exists(file_path):
        os.remove(file_path)

    try:
        # Generate speech audio using edge_tts
        communicate = edge_tts.Communicate(text, AssistantVoice, pitch='+5Hz', rate='+13%')
        await communicate.save(file_path)  # Save the generated speech
    except Exception as e:
        print(f"Error in text-to-speech conversion: {e}")

# Function to play the generated audio file
def TTS(text, func=lambda r=None: True):
    try:
        # Convert text to an audio file
        asyncio.run(TextToAudioFile(text))

        # Initialize pygame mixer
        pygame.mixer.init()
        pygame.mixer.music.load("Data/speech.mp3")
        pygame.mixer.music.play()

        # Wait until the audio finishes playing
        while pygame.mixer.music.get_busy():
            if func() == False:
                break
            pygame.time.Clock().tick(10)

        return True

    except Exception as e:
        print(f"Error in TTS: {e}")

    finally:
        try:
            func(False)
            pygame.mixer.music.stop()
            pygame.mixer.quit()  # Quit pygame only if initialized
        except Exception as e:
            print(f"Error in cleanup: {e}")

# Function to manage TTS with additional responses for long text
def TextToSpeech(text, func=lambda r=None: True):
    sentences = text.split(".")  # Split the text by periods

    # Predefined responses for long text
    responses = [
        "The rest of the text is on the chat screen, sir.",
        "Sir, check the chat screen for the complete answer.",
        "You'll find the full text in the chat, sir.",
        "Sir, please review the chat for more details."
    ]

    # If the text is long, summarize and provide additional info
    if len(sentences) > 4 and len(text) >= 250:
        TTS(" ".join(sentences[:2]) + ". " + random.choice(responses), func)
    else:
        TTS(text, func)

# Main execution loop
if __name__ == "__main__":
    while True:
        user_text = input("Enter the text: ")
        if user_text.lower() in ["exit", "quit", "bye"]:
            print("Exiting program.")
            break
        TextToSpeech(user_text)
