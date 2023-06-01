import string
import random
import requests
import os
import threading

api = "https://discordapp.com/api/v9/entitlements/gift-codes/"
api2 = "?with_application=false&with_subscription_plan=true"
url = "https://discord.com/gifts/"

if os.name == "nt":
    os.system("cls")
    os.system("title By @rxyzqc")

proxy_url = input("Proxy URL: ")
chars = string.ascii_letters + string.digits

if proxy_url:
    proxy_response = requests.get(proxy_url)
    proxy_list = proxy_response.text.strip().split("\n")
    proxies = [proxy.split()[0] for proxy in proxy_list]
    print(len(proxies), "proxies found")
else:
    proxy_response = requests.get(
        "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity"
        "=all&simplified=true"
    )
    proxy_list = proxy_response.text.strip().split("\n")
    proxies = [proxy.split()[0] for proxy in proxy_list]
    print(len(proxies), "proxies found")

print('')

lock = threading.Lock()  # Lock for thread-safe writing to file


def check_code(code, proxy):
    code_url = api + code + api2

    proxy_url = f'http://{proxy}'

    proxy_config = {
        'http': proxy_url,
        'https': proxy_url
    }

    try:
        r = requests.get(code_url, proxies=proxy_config, timeout=10)
        rs = r.status_code

        with lock:  # Acquire lock before writing to file
            if rs == 200:
                print(f"\033[32mValid\033[0m \033[34m|\033[0m {code} \033[34m|\033[0m {proxy}")
                with open("valid_codes.txt", "a") as f:
                    f.write(url + code + "\n")
            elif rs == 404:
                print(f"\033[31mInvalid\033[0m \033[34m|\033[0m {code} \033[34m|\033[0m {proxy}")
            elif rs == 429:
                print(f"\033[93mTimeout\033[0m \033[34m|\033[0m {code} \033[34m|\033[0m {proxy}")
            else:
                print(f"\033[35mError\033[0m \033[34m|\033[0m {code} \033[34m|\033[0m {proxy}")
    except requests.RequestException:
        print(f"\033[35mError\033[0m   \033[34m|\033[0m {code} \033[34m|\033[0m {proxy}")


def main():
    while True:
        code = "".join(random.choice(chars) for _ in range(16))
        proxy = random.choice(proxies)
        t = threading.Thread(target=check_code, args=(code, proxy))
        t.start()


main()
