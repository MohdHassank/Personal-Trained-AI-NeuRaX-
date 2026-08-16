from groq import Groq  # Importing the Groq library to use its API
from json import load, dump  # Importing functions to read and write JSON files
import datetime  # Importing datetime module for real-time information
from dotenv import load_dotenv  # Importing load_dotenv to read .env file
import os  # Importing os to access environment variables

# ✅ Load the .env file from the JARVIS_AI folder (one level up from Backend)
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
load_dotenv(env_path)

# ✅ Retrieve environment variables correctly
Username = os.getenv("Username")
Assistantname = os.getenv("Assistantname")
GroqAPIKey = os.getenv("GROQ_API_KEY") or os.getenv("GroqAPIKey")

# ✅ Ensure API key is provided
if not GroqAPIKey:
    raise ValueError("Error: GROQ_API_KEY is missing. Please check your .env file.")

# ✅ Initialize the Groq client
client = Groq(api_key=GroqAPIKey)

# ✅ Ensure the Data folder exists
chat_log_path = "Data/ChatLog.json"
os.makedirs("Data", exist_ok=True)

# ✅ Load existing chat logs or create a new empty list
try:
    with open(chat_log_path, "r") as f:
        messages = load(f)
except (FileNotFoundError, ValueError):
    messages = []
    with open(chat_log_path, "w") as f:
        dump(messages, f)

# ✅ Function to get real-time date and time information
def RealtimeInformation():
    current_date_time = datetime.datetime.now()
    return f"""Please use this real-time information if needed,
Day: {current_date_time.strftime('%A')}
Date: {current_date_time.strftime('%d')}
Month: {current_date_time.strftime('%B')}
Year: {current_date_time.strftime('%Y')}
Time: {current_date_time.strftime('%H:%M:%S')}"""

# ✅ Function to format chatbot responses
def AnswerModifier(answer):
    return "\n".join([line.strip() for line in answer.split("\n") if line.strip()])

# ✅ System Message Configuration
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
* Do not tell time until I ask, do not talk too much, just answer the question. *
* Reply in only English, even if the question is in Hindi, reply in English. *
* Do not provide notes in the output, just answer the question and never mention your training data. *
"""

SystemChatBot = [{"role": "system", "content": System}]

# ✅ Main chatbot function
def ChatBot(query):
    """Sends the user's query to the chatbot and returns the AI's response."""
    
    try:
        # Load the latest chat log
        with open(chat_log_path, "r") as f:
            messages = load(f)

        # Append the user's query
        messages.append({"role": "user", "content": query})

        # ✅ Make a request to the Groq API
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=SystemChatBot + [{"role": "system", "content": RealtimeInformation()}] + messages,  # Include system instructions & chat history
            max_tokens=1024,  # Limit max response length
            temperature=0.7,  # Adjust randomness of responses
            top_p=1,  # Use nucleus sampling
            stream=False  # Disable streaming for proper response handling
        )

        # ✅ Extract AI response
        answer = completion.choices[0].message.content.strip()

        # ✅ Append chatbot response to messages
        messages.append({"role": "assistant", "content": answer})

        # ✅ Save updated chat log
        with open(chat_log_path, "w") as f:
            dump(messages, f, indent=4)

        return AnswerModifier(answer)

    except Exception as e:
        print(f"Error: {e}")
        return "Sorry, something went wrong."

# ✅ Main program entry point
if __name__ == "__main__":
    while True:
        user_input = input("Enter your question: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Goodbye!")
            break
        print(ChatBot(user_input))
