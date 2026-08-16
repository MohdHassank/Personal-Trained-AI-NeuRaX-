from googlesearch import search  # Import Google Search
from groq import Groq  # Import the Groq library
from json import load, dump  # JSON functions for file handling
import datetime  # For real-time date and time information
from dotenv import dotenv_values  # Read environment variables from .env
import requests  # Fetch webpage content
from bs4 import BeautifulSoup  # Extract information from web pages

# Load environment variables
env_vars = dotenv_values(".env")

# Retrieve credentials
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GROQ_API_KEY") or env_vars.get("GroqAPIKey")

# Initialize Groq client
client = Groq(api_key=GroqAPIKey)

# System instructions
System = f"""Hello, I am {Username}. You are {Assistantname}, an advanced AI chatbot with real-time internet access.
*** Provide answers in a professional way using proper grammar, punctuation, and clarity. ***"""

# Load chat log or create an empty one if missing
try:
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)
except Exception:
    with open(r"Data\ChatLog.json", "w") as f:
        dump([], f)
        messages = []  # Initialize an empty list if file doesn't exist

# Function to fetch webpage content
def ExtractContentFromURL(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            paragraphs = soup.find_all("p")
            text_content = "\n".join([para.get_text() for para in paragraphs[:5]])  # Extract first 5 paragraphs
            return text_content
        else:
            return "Could not fetch data from the website."
    except Exception:
        return "Error fetching data from the website."

# Function to perform Google Search and extract content
def GoogleSearch(query):
    try:
        results = list(search(query, num_results=3))  # Get top 3 search results
        Answer = "Extracted information:\n[start]\n"

        for url in results:
            Answer += ExtractContentFromURL(url) + "\n\n"  # Extract content from each link

        Answer += "[end]"
        return Answer
    except Exception as e:
        return f"Error performing Google search: {e}"

# Function to clean the response
def AnswerModifier(Answer):
    return '\n'.join([line for line in Answer.split('\n') if line.strip()])

# System chatbot template
SystemChatBot = [
    {"role": "system", "content": System},
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello, how can I help you?"}
]

# Function to get real-time information
def Information():
    now = datetime.datetime.now()
    return f"""Use This Real-time Information if needed:
Day: {now.strftime("%A")}
Date: {now.strftime("%d")}
Month: {now.strftime("%B")}
Year: {now.strftime("%Y")}
Time: {now.strftime("%H:%M:%S")}"""

# Function to handle real-time queries
def RealtimeSearchEngine(prompt):
    global SystemChatBot, messages

    # Load existing chat log
    try:
        with open(r"Data\ChatLog.json", "r") as f:
            messages = load(f)
    except Exception:
        messages = []  # Initialize an empty list if file read fails

    messages.append({"role": "user", "content": prompt})

    # Extract information from search results
    extracted_info = GoogleSearch(prompt)
    SystemChatBot.append({"role": "system", "content": extracted_info})

    # Generate AI response based on extracted information
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=SystemChatBot + [{"role": "system", "content": Information()}] + messages,
            temperature=0.7,
            max_tokens=2048,
            top_p=1,
            stream=True,
            stop=None
        )

        Answer = ""

        # Collect response chunks
        for chunk in completion:
            if hasattr(chunk.choices[0].delta, "content") and chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content

        Answer = Answer.strip().replace("</s>", "")
        messages.append({"role": "assistant", "content": Answer})

        # Save updated chat log
        with open(r"Data\ChatLog.json", "w") as f:
            dump(messages, f, indent=4)

        # Remove last system message
        SystemChatBot.pop()
        
        return AnswerModifier(Answer)
    
    except Exception as e:
        return f"Error generating AI response: {e}"

# Main loop
if __name__ == "__main__":
    while True:
        prompt = input("Enter your query: ")
        if prompt.lower() in ["exit", "quit"]:
            print("Exiting chatbot...")
            break
        print(RealtimeSearchEngine(prompt))
