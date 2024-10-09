import time
import json
import random
from mimetypes import guess_type
from typing import List, Dict
from openai_client import use_azure_openai_client


def read_products() -> List[Dict]:
    with open('products.json', 'r', encoding='utf-8') as file:
        products = json.load(file)

    random.shuffle(products)

    return products

def get_new_prompt(text: str, categories_str: str, bad_prompts: List[str]) -> str:
    prompt = f"You are a prompt creation assistant. Your task is to modify the provided prompt to make it better suited for categorizing a product into one of the predefined categories: {categories_str}. The modified prompt must instruct the assistant to return the category name as a one-word answer based on the product description. Provide the new, ready-to-use prompt as a single-line answer. Avoid generating similar prompts, and do not use the following prompts: {', '.join(bad_prompts)}"
    text = f"Prompt: {text}"
    new_prompt = use_azure_openai_client(
        prompt=prompt, text=text, temperature=0.7
    )
    print(f"new prompt = {new_prompt}")
    return new_prompt

def main():
    products = read_products()

    unique_categories = {product['category'] for product in products}
    unique_categories_list = list(unique_categories)
    categories_str = ', '.join(unique_categories_list)

    prompt = f"You are an assistant that classifies products based on their description. Your task is to assign the product to one of the predefined categories such as {categories_str}, based only on the provided description. Provide the category name as a one-word answer."
    guessed = 0
    guessed_in_a_row = 0
    prompts_stat = []
    bad_prompts = []

    for product in products:
        category = product.get('category')
        description = product.get('description')
        predicted_category = use_azure_openai_client(
            prompt=prompt, text=description
        )

        print(f"Predicted category: {predicted_category}, actual category: {category}")

        if category.lower() == predicted_category.lower():
            guessed += 1
            guessed_in_a_row += 1
        else:
            prompts_stat.append({
                "prompt": prompt,
                "quessed": guessed_in_a_row
            })

            guessed_in_a_row = 0
            bad_prompts.append(prompt)

            prompt = get_new_prompt(
                prompt, categories_str, bad_prompts
            )

        time.sleep(1)

    if len(prompts_stat) > 0:
        with open('prompts_stat.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(prompts_stat, ensure_ascii=False, indent=4))

    print(f"Guessed: {guessed} from {len(products)} products")

if __name__ == '__main__':
    main()