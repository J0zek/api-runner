import os
import time
import random
import requests


def call_api_a(api_key, hermes_model, system_content, user_content):
    url = "https://inference-api.nousresearch.com/v1/chat/completions"
    payload = {
        "model": f"{hermes_model}",
        "messages": [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ],
        "max_tokens": 2048
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        parsed = response.json()
        return parsed["choices"][0]["message"]["content"].replace("\n", "")
    except Exception as e:
        print(f"[API A Error]: {e}")
        return None


def call_api_b(api_key, model, user_content):
    url = "https://openrouter.ai/api/v1/chat/completions"
    payload = {
        "model": f"@preset/{model}",
        "messages": [{"role": "user", "content": user_content}]
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        parsed = response.json()
        return parsed["choices"][0]["message"]["content"].replace("\n", "")
    except Exception as e:
        print(f"[API B Error]: {e}")
        return None


def pop_random_start(path: str):
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    if not lines:
        return None
    i = random.randrange(len(lines))
    line = lines.pop(i).rstrip("\n")
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    return line


def run_loop(api_key_a, api_key_b, hermes_model, system_content, model, initial_content, max_steps=10):
    user_content = initial_content
    step = 0

    while step < max_steps:
        exit_prob = step / max_steps
        if random.random() < exit_prob:
            break

        sleep_time = random.randint(30, 120)
        time.sleep(sleep_time)

        if step % 2 == 0:
            user_content = call_api_a(api_key_a, hermes_model, system_content, user_content)
        else:
            user_content = call_api_b(api_key_b, model, user_content)
            
        print(user_content, "\n\n")
        
        if user_content is None:
            print("API call failed. Breaking the loop.")
            break

        step += 1


def main():
    api_key_a = os.environ.get("API_KEY_A")
    api_key_b = os.environ.get("API_KEY_B")
    system_a = os.environ.get("SYSTEM_A")
    hermes_model = os.environ.get("HERMES_MODEL")
    model = os.environ.get("MODEL")

    start_text = pop_random_start("start_questions.txt")
    if start_text is None:
        print("start_questions.txt is empty")
        return None

    run_loop(api_key_a, api_key_b, hermes_model, system_a, model, start_text)


if __name__ == "__main__":
    main()






