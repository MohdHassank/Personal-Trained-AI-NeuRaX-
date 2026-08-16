import asyncio
from random import randint
from PIL import Image
import requests
from dotenv import load_dotenv
import os
from time import sleep

# Load environment variables
load_dotenv()
API_KEY = os.getenv("HuggingFaceAPIKey") or os.getenv("HuggingFacAPIKey")

# Ensure "Data" folder exists
os.makedirs("Data", exist_ok=True)

# API details for Hugging Face Stable Diffusion
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {API_KEY}"}

# Function to open and display images
def open_images(prompt):
    folder_path = "Data"
    prompt = prompt.replace(" ", "_")
    Files = [f"{prompt}{i}.jpg" for i in range(1, 5)]

    for jpg_file in Files:
        image_path = os.path.join(folder_path, jpg_file)
        try:
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()
            sleep(1)
        except IOError:
            print(f"Unable to open {image_path}")

# Async function to query the API
async def query(payload):
    response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
    return response.content

# Async function to generate images
async def generate_images(prompt: str):
    tasks = []
    for i in range(4):
        payload = {
            "inputs": f"{prompt}, quality=4K, sharpness=maximum, Ultra High details, high resolution, seed = {randint(0, 1000000)}"
        }
        tasks.append(asyncio.create_task(query(payload)))

    image_bytes_list = await asyncio.gather(*tasks)

    # Save images
    for i, image_bytes in enumerate(image_bytes_list):
        with open(f"Data/{prompt.replace(' ', '_')}{i + 1}.jpg", "wb") as f:
            f.write(image_bytes)

# Wrapper function to call image generation and display
def GenerateImages(prompt: str):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(generate_images(prompt))
    open_images(prompt)

# Main Loop to check requests
while True:
    try:
        with open("Frontend/Files/ImageGeneration.data", "r") as f:
            Data: str = f.read()

        Prompt, Status = Data.split(",")

        if Status == "True":
            print("Generating Images...")
            GenerateImages(prompt=Prompt)

            # Reset status after generating images
            with open("Frontend/Files/ImageGeneration.data", "w") as f:
                f.write("False,False")
            break  # Exit loop after one request

        else:
            sleep(1)  # Wait before checking again

    except Exception as e:
        print(f"Error: {e}")
