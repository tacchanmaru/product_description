import os
import openai

openai.api_key = os.environ.get("OPENAI_API_KEY")

def get_response(system_prompt, user_prompt):
    response = openai.ChatCompletion.create(
        model = "gpt-4-1106-preview",
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message.content

def main():

    with open("./system_prompts/young.txt") as f:
        system_prompt_young = f.read()

    with open("./system_prompts/elderly.txt") as f:
        system_prompt_elderly = f.read()


    items = ['ladies_bag_1', 'ladies_bag_2', 'ladies_bag_3', 'mens_jacket_outer_1', 'mens_jacket_outer_2', 'mens_jacket_outer_3']

    for item in items:
        with open("../product_info/" + item + '.txt', mode='r') as g:
            contents_sheet = g.read()
    
        while(True):
            res_young = get_response(system_prompt_young, contents_sheet)
            print(len(res_young))
            if 350 < len(res_young) < 450:
                break

        with open("./description/young_" + item + '.txt', mode="w") as g:
            g.write(res_young)

        while(True):
            res_elderly = get_response(system_prompt_elderly, contents_sheet)
            print(len(res_elderly))
            if 350 < len(res_elderly) < 450:
                break

        with open("./description/elderly_" + item + '.txt', mode="w") as g:
            g.write(res_elderly)


if __name__ == "__main__":
    main()