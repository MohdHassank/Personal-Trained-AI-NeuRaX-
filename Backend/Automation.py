# Import required libraries
from AppOpener import close, open as appopen
from webbrowser import open as webopen
from pywhatkit import search, playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
import webbrowser
import subprocess
import requests
import keyboard
import asyncio
import os

# Load environment variables
env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GROQ_API_KEY") or env_vars.get("GroqAPIKey")

# Define user-agent for requests
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

# Initialize Groq Client
client = Groq(api_key=GroqAPIKey)

# List to store chatbot messages
messages = []

# System message for chatbot
SystemChatBot = [{"role": "system", "content": f"Hello, I am {os.environ.get('Username', 'Assistant')}, You're a content writer."}]

# Function to perform a Google search
def GoogleSearch(Topic):
    search(Topic)
    return True

# Function to generate content using AI
def Content(Topic):
    Topic = Topic.replace("Content ", "")

    def OpenNotepad(File):
        subprocess.Popen(['notepad.exe', File])

    def ContentWriterAI(prompt):
        messages.append({"role": "user", "content": f"{prompt}"})
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=SystemChatBot + messages,
            max_tokens=2048,
            temperature=0.7,
            top_p=1
        )

        answer = completion.choices[0].message.content
        answer = answer.replace("</s>", "")
        messages.append({"role": "assistant", "content": answer})
        return answer

    ContentByAI = ContentWriterAI(Topic)

    file_path = rf"Data\{Topic.lower().replace(' ', '')}.txt"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(ContentByAI)

    OpenNotepad(file_path)
    return True

# Function to search YouTube
def YouTubeSearch(Topic):
    webbrowser.open(f"https://www.youtube.com/results?search_query={Topic}")
    return True

# Function to play a YouTube video
def PlayYoutube(query):
    playonyt(query)
    return True

# Function to open an application or webpage
def OpenApp(app, sess=requests.Session()):
    try:
        appopen(app, match_closest=True, output=True, throw_error=True)
        return True
    except:
        def extract_links(html):
            if html is None:
                return []
            soup = BeautifulSoup(html, 'html.parser')
            links = soup.find_all('a', {'jsname': 'UWckNb'})
            return [link.get('href') for link in links]

        def search_google(query):
            url = f"https://www.google.com/search?q={query}"
            headers = {"User-Agent": useragent}
            response = sess.get(url, headers=headers)
            return response.text if response.status_code == 200 else None

        html = search_google(app)
        links = extract_links(html)

        if links:
            webopen(links[0])
            return True
        return False

# Function to close an application
def CloseApp(app):
    try:
        close(app, match_closest=True, output=True, throw_error=True)
        return True
    except:
        return False

# Function to execute system commands
def System(command):
    actions = {
        "mute": lambda: keyboard.press_and_release("volume mute"),
        "unmute": lambda: keyboard.press_and_release("volume mute"),
        "volume up": lambda: keyboard.press_and_release("volume up"),
        "volume down": lambda: keyboard.press_and_release("volume down")
    }

    if command in actions:
        actions[command]()
        return True
    return False

# Asynchronous function to translate and execute commands
async def TranslateAndExecute(commands: list[str]):
    funcs = []
    for command in commands:
        if command.startswith("open "):
            if command not in ["open it", "open file"]:
                funcs.append(asyncio.to_thread(OpenApp, command.removeprefix("open ")))

        elif command.startswith("close "):
            funcs.append(asyncio.to_thread(CloseApp, command.removeprefix("close ")))

        elif command.startswith("play "):
            funcs.append(asyncio.to_thread(PlayYoutube, command.removeprefix("play ")))

        elif command.startswith("content "):
            funcs.append(asyncio.to_thread(Content, command.removeprefix("content ")))

        elif command.startswith("google search "):
            funcs.append(asyncio.to_thread(GoogleSearch, command.removeprefix("google search ")))

        elif command.startswith("youtube search "):
            funcs.append(asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search ")))

        elif command.startswith("system "):
            funcs.append(asyncio.to_thread(System, command.removeprefix("system ")))

        else:
            print(f"No Function Found for {command}")

    results = await asyncio.gather(*funcs)
    return results

# Asynchronous function to automate commands execution
async def Automation(commands: list[str]):
    results = await TranslateAndExecute(commands)
    return all(results)  # Returns True if all commands executed successfully


