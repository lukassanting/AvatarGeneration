# ! DISCLAIMER !
# Not my idea originally, based on an & uses code from  article by Real Python
# Link to original article: https://realpython.com/generate-images-with-dalle-openai-api/

# Imports
import json
import os
import sys
from base64 import b64decode
from pathlib import Path
from art_avatar_generator import convert_data_to_image

import openai


def generate_variations_from_image(file_name):
    data_dir = Path.cwd() / "responses"
    source_file = data_dir / file_name

    openai.api_key = os.getenv("OPENAI_API_KEY")

    with open(source_file, mode="r", encoding="utf-8") as json_file:
        saved_response = json.load(json_file)
        image_data = b64decode(saved_response["data"][0]["b64_json"])

    n_images = int(input("How many images do you want to generate?"))
    image_size = input("Provide a size for the images, e.g. 256x256: ")

    response = openai.Image.create_variation(
        image=image_data,
        n=n_images,
        size=image_size,
        response_format="b64_json",
    )

    new_file_name = f"vary-{source_file.stem[:5]}-{response['created']}.json"

    with open(data_dir / new_file_name, mode="w", encoding="utf-8") as file:
        json.dump(response, file)

    convert_data_to_image(new_file_name)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        generate_variations_from_image(
            input("Please provide a .json file to convert: "))
    elif len(sys.argv) > 2:
        generate_variations_from_image(
            input("Too many arguments provided. Please provide a .json file to convert: "))
    else:
        generate_variations_from_image(sys.argv[1:][0])
