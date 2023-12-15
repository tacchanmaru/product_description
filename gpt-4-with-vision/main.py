import base64
import requests
import os

# OpenAI API Key
api_key = os.getenv("OPENAI_API_KEY")

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def get_response(system_prompt, user_prompt, base64_image, headers):
    payload = {
        "model": "gpt-4-vision-preview",
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

    print(response.json())
    return response.json()['choices'][0]['message']['content']

def main():
    with open("./system_prompts/young.txt") as f:
        system_prompt_young = f.read()

    with open("./system_prompts/elderly.txt") as f:
        system_prompt_elderly = f.read()

    items = ['ladies_bag_1', 'ladies_bag_2', 'ladies_bag_3', 'mens_jacket_outer_1', 'mens_jacket_outer_2', 'mens_jacket_outer_3']
    
    for item in items:
        with open("../product_info/" + item + ".txt") as g:
            contents_sheet = g.read()

        # Path to your image
        image_path = "../product_info/" + item + ".jpg"

        # Getting the base64 string
        base64_image = encode_image(image_path)
    
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        while(True):
            res_young = get_response(system_prompt_young, contents_sheet, base64_image, headers)
            print(len(res_young))
            if 350 < len(res_young) < 450:
                break

        with open("./description/young_" + item + ".txt", mode="w") as g:
            g.write(res_young)

        while(True):
            res_elderly = get_response(system_prompt_elderly, contents_sheet, base64_image, headers)
            print(len(res_elderly))
            if 350 < len(res_elderly) < 450:
                break

        with open("./description/elderly_" + item + ".txt", mode="w") as g:
            g.write(res_elderly)

if __name__ == "__main__":
    main()