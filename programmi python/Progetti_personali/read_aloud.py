import pyttsx3

def read_aloud(text):
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()

    # Set properties (optional)
    engine.setProperty('rate', 150)  # Speed of speech

    # Speak the given text
    engine.say(text)

    # Wait for the speech to finish
    engine.runAndWait()

if __name__ == "__main__":
    # Example usage
    text_to_read = "Hello, this is an example text to be read aloud."
    read_aloud(text_to_read)
