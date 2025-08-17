# import aiohttp
# from aiohttp_socks import ProxyConnector
# import asyncio
# import json
# import random


# async def get_session(proxy: str or None):
#     if proxy:
#         connector = ProxyConnector.from_url(proxy)
#     else:
#         connector = aiohttp.TCPConnector()
#     return aiohttp.ClientSession(connector=connector)


# async def call_api_a(api_key, hermes_model, system_content, user_content, user_agent=None, proxy=None):
#     url = "https://inference-api.nousresearch.com/v1/chat/completions"
#     payload = {
#         "model": f"{hermes_model}",
#         "messages": [
#             {"role": "system", "content": system_content},
#             {"role": "user", "content": user_content}
#         ],
#         "max_tokens": 2048
#     }
#     headers = {
#         "Authorization": f"Bearer {api_key}",
#         "Content-Type": "application/json"
#     }
#     if user_agent:
#         headers["User-Agent"] = user_agent

#     try:
#         async with await get_session(proxy) as session:
#             async with session.post(url, json=payload, headers=headers) as response:
#                 parsed = await response.json()
#                 content = parsed["choices"][0]["message"]["content"]
#                 return content.replace("\n", "")
#     except aiohttp.ClientError as e:
#         print(f"[API A Error] Request failed: {e}")
#         return None
#     except Exception as e:
#         print(f"[API A Error]: {e}")
#         return None


# async def call_api_b(api_key, model, user_content, user_agent=None, proxy=None):
#     url = "https://openrouter.ai/api/v1/chat/completions"
#     payload = {
#         "model": f"@preset/{model}",
#         "messages": [{"role": "user", "content": user_content}]
#     }
#     headers = {
#         "Authorization": f"Bearer {api_key}",
#         "Content-Type": "application/json"
#     }
#     if user_agent:
#         headers["User-Agent"] = user_agent

#     try:
#         async with await get_session(proxy) as session:
#             async with session.post(url, json=payload, headers=headers) as response:
#                 parsed = await response.json()
#                 content = parsed["choices"][0]["message"]["content"]
#                 return content.replace("\n", "")
#     except aiohttp.ClientError as e:
#         print(f"[API B Error] Request failed: {e}")
#         return None
#     except Exception as e:
#         print(f"[API B Error]: {e}")
#         return None


# async def run_loop(api_key_a, api_key_b, hermes_model, system_content, model, initial_content, user_agent=None, proxy=None, max_steps=5):
#     user_content = initial_content
#     step = 0

#     while step < max_steps:
#         exit_prob = step / max_steps
#         if random.random() < exit_prob:
#             break
        
#         sleep_time = random.randint(30, 120)
#         await asyncio.sleep(sleep_time)
        
#         if step % 2 == 0:
#             user_content = await call_api_a(api_key_a, hermes_model, system_content, user_content, user_agent, proxy)
#         else:
#             user_content = await call_api_b(api_key_b, model, user_content, user_agent, proxy)

#         if user_content is None:
#             print(f"API call failed. Breaking the loop.")
#             break

#         step += 1


# def pop_random_start(path: str):
#     with open(path, "r", encoding="utf-8") as f:
#         lines = f.readlines()
#     if not lines:
#         return None
#     i = random.randrange(len(lines))
#     line = lines.pop(i).rstrip("\n")
#     with open(path, "w", encoding="utf-8") as f:
#         f.writelines(lines)
#     return line


# async def run_account(account):
#     api_key_a_str = account[0]
#     api_key_b_str = account[1]
#     system_a = account[2]
#     hermes_model = account[3]
#     model = account[4]
#     user_agent_str = account[5]
#     proxy_str = account[6]

#     while True:
#         start_text = pop_random_start("start_questions.txt")
#         if start_text is None:
#             print(f"start_questions.txt is empty")
#             break

#         await run_loop(api_key_a_str, api_key_b_str, hermes_model, system_a, model, start_text, user_agent_str, proxy_str)
#         sleep_time = random.randint(8 * 3600, 48 * 3600)
#         await asyncio.sleep(sleep_time)


# async def main():
#     accounts = []

#     with open("accounts.txt", "r", encoding="utf-8") as file:
#         for line in file:
#             line = line.strip()
#             if not line:
#                 continue

#             parts = line.split("|")

#             if parts[-1] == "None":
#                 parts[-1] = None

#             accounts.append(parts)
            
#     tasks = [run_account(acc) for acc in accounts]
#     await asyncio.gather(*tasks)


# if __name__ == "__main__":
#     asyncio.run(main())

import os
import time
import random
import requests


def call_api_a(api_key, hermes_model, system_content, user_content, user_agent=None):
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
    if user_agent:
        headers["User-Agent"] = user_agent

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        parsed = response.json()
        return parsed["choices"][0]["message"]["content"].replace("\n", "")
    except Exception as e:
        print(f"[API A Error]: {e}")
        return None


def call_api_b(api_key, model, user_content, user_agent=None):
    url = "https://openrouter.ai/api/v1/chat/completions"
    payload = {
        "model": f"@preset/{model}",
        "messages": [{"role": "user", "content": user_content}]
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    if user_agent:
        headers["User-Agent"] = user_agent

    try:
        response = requests.post(url, json=payload, headers=headers, proxies=proxies, timeout=60)
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


def run_loop(api_key_a, api_key_b, hermes_model, system_content, model, initial_content, user_agent=None, max_steps=5):
    user_content = initial_content
    step = 0

    while step < max_steps:
        exit_prob = step / max_steps
        if random.random() < exit_prob:
            break

        sleep_time = random.randint(30, 120)
        time.sleep(sleep_time)

        if step % 2 == 0:
            user_content = call_api_a(api_key_a, hermes_model, system_content, user_content, user_agent)
        else:
            user_content = call_api_b(api_key_b, model, user_content, user_agent)

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
    user_agent = os.environ.get("USER_AGENT")

    while True:
        start_text = pop_random_start("start_questions.txt")
        if start_text is None:
            print("start_questions.txt is empty")
            break

        run_loop(api_key_a, api_key_b, hermes_model, system_a, model, start_text, user_agent, proxy)


if __name__ == "__main__":
    main()