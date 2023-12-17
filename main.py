import sys
from openai import OpenAI
import base64
import requests
import os


# OpenAI API Key
api_key = os.getenv("OPENAI_API_KEY")

items = ['ladies_bag_1', 'ladies_bag_2', 'ladies_bag_3', 'mens_jacket_outer_1', 'mens_jacket_outer_2', 'mens_jacket_outer_3']


# openai chat api

def get_response_gpt_4_turbo(system_prompt, user_prompt):
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        temperature = 0,
        messages=[
            {"role": "system", "content":system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message.content

def get_response_gpt_4_with_vision(system_prompt, user_prompt, base64_image, headers):
    payload = {
        "model": "gpt-4-vision-preview",
        "temperature": 0,
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": user_prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 4096
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    return response.json()['choices'][0]['message']['content']



# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    

def gpt_4_turbo():

    with open("./gpt-4-trubo/system_prompts/young.txt") as f:
        system_prompt_young = f.read()

    with open("./gpt-4-trubo/system_prompts/elderly.txt") as f:
        system_prompt_elderly = f.read()


    for item in items:
        with open("./product_info/" + item + '.txt', mode='r') as g:
            contents_sheet = g.read()

        res_young = get_response_gpt_4_turbo(system_prompt_young, contents_sheet)
        print(len(res_young))

        with open("./gpt-4-trubo/description/young_" + item + '.txt', mode="w") as g:
            g.write(res_young)

        res_elderly = get_response_gpt_4_turbo(system_prompt_elderly, contents_sheet)
        print(len(res_elderly))

        with open("./gpt-4-trubo/description/elderly_" + item + '.txt', mode="w") as g:
            g.write(res_elderly)


def gpt_4_with_vision():
    with open("./gpt-4-with-vision/system_prompts/young.txt") as f:
        system_prompt_young = f.read()

    with open("./gpt-4-with-vision/system_prompts/elderly.txt") as f:
        system_prompt_elderly = f.read()

    for item in items:
        with open("./product_info/" + item + ".txt") as g:
            contents_sheet = g.read()

        # Path to your image
        image_path = "./product_info/" + item + ".jpg"

        # Getting the base64 string
        base64_image = encode_image(image_path)
    
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        
        res_young = get_response_gpt_4_with_vision(system_prompt_young, contents_sheet, base64_image, headers)
        print(len(res_young))

        with open("./gpt-4-with-vision/description/young_" + item + ".txt", mode="w") as g:
            g.write(res_young)

        res_elderly = get_response_gpt_4_with_vision(system_prompt_elderly, contents_sheet, base64_image, headers)
        print(len(res_elderly))

        with open("./gpt-4-with-vision/description/elderly_" + item + ".txt", mode="w") as g:
            g.write(res_elderly)


def main(folder):

    if folder == "gpt-4-turbo":
        gpt_4_turbo()

    if folder == "gpt-4-with-vision":
        gpt_4_with_vision()

    else:
        print("Usage: python3 main.py folder_name")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 main.py folder_name")
        sys.exit(1)
    folder = sys.argv[1]
    main(folder)
