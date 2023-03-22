# ! DISCLAIMER !
# Not my idea originally, based on & uses code from an article by Real Python
# Link to original article: https://realpython.com/generate-images-with-dalle-openai-api/

# Imports
import json
import os
import openai
from base64 import b64decode
from pathlib import Path
import sys


def generate_image_from_prompt():
    '''
    Function to take a prompt and request the openai dall-e to create an image with that prompt
    '''

    # input
    input_prompt = input("Provide a sentence to generate an image from: ")
    n_images = int(input("How many images do you want to generate?"))
    image_size = input("Provide a size for the images, e.g. 256x256: ")

    # directory
    output_dir = Path.cwd() / "responses"
    output_dir.mkdir(exist_ok=True)

    # get api key (make sure to follow steps in "commands_to_run" to get this to work)
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # generate image
    response = openai.Image.create(
        prompt=input_prompt,
        n=n_images,
        size=image_size,
        response_format="b64_json"
    )

    file_name = output_dir / f"{input_prompt[:5]}-{response['created']}.json"

    with open(file_name, mode="w", encoding="utf-8") as file:
        json.dump(response, file)

    convert_data_to_image(file_name)


def convert_data_to_image(file_name):
    '''
    Function to take a json file containing an encoded image & save the image as a .png
    '''

    # get files and paths
    data_dir = Path.cwd() / "responses"
    json_file = data_dir / file_name
    image_dir = Path.cwd() / "images" / json_file.stem

    image_dir.mkdir(parents=True, exist_ok=True)

    # open file to convert
    with open(json_file, mode="r", encoding="utf-8") as file:
        response = json.load(file)

    # decode image from encoded text and save to .png file
    for index, image_dict in enumerate(response["data"]):
        image_data = b64decode(image_dict["b64_json"])
        image_file = image_dir / f"{json_file.stem}-{index}.png"
        with open(image_file, mode="wb") as png:
            png.write(image_data)


if __name__ == "__main__":
    generate_image_from_prompt()
