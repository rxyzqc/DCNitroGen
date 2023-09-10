import concurrent.futures
import os
import platform
import random
import socket
import string
import threading

import requests
from discord_webhook import DiscordWebhook, DiscordEmbed

api = "https://discordapp.com/api/v9/entitlements/gift-codes/"
api2 = "?with_application=false&with_subscription_plan=true"
url = "https://discord.com/gifts/"


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def update_title(title):
    os.system(f"title {title}" if os.name == "nt" else f"echo -n -e '\033]0;{title}\a'")


clear()

print("""
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@\033[34m#######################################\033[0m%@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@\033[34m#############################################\033[0m@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@\033[34m##############################################\033[0m@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\033[34m##########(///////////(#############\033[0m%@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\033[34m######///////(&@@@&(///////###########\033[0m&@@@@@@
@@@@\033[34m***@@@@@@@@@\033[34m######################/////@@@           @@@/////##########\033[0m@@@@@
@@@\033[34m/****@@@@@@@\033[34m#####################////@@.                 .@@////#########\033[0m@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\033[34m%####(///@@      .,,,,,,,,,       @@///#########\033[0m@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\033[34m####///@@      ,,,,,,,,,,,,,      @@///########\033[0m%@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@\033[34m%####///#@      ,,,,,,,,,,,,,,,      @(///########\033[0m@@
@@@@@@@@@@@@@@@@@@@@\033[34m#############///@@    .,,,,,,,,,,,,,,,,,     @@///########\033[0m@@
@@@@@@@@@@@@@@@@@@@@@@@@@\033[34m########///#@      ,,,,,,,,,,,,,,,      @(///########\033[0m@@
@@@@@@@@@@@@@@@@@@@@@@@@@\033[34m#########///@@      ,,,,,,,,,,,,,      @@///########\033[0m%@@
@@@@@@@@@@@@@@@@@@@@@@@@@@\033[34m#########///@@      .,,,,,,,,,      .@&///#########\033[0m@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@\033[34m#########////@@,                 (@@////#########\033[0m@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@\033[34m##########/////@@@.         *@@@/////##########\033[0m@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&\033[34m###########////////%&&&%////////###########\033[0m@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&@%\033[34m##############//////////(##############\033[0m&@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\033[34m###################################\033[0m@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\033[34m############################\033[0m&@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&\033[34m#################\033[0m@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
""")

input("Press enter to start . . .")
clear()

ask_webhook = input("Use discord webhook? (y/n): ").lower()
clear()

webhook_url = input("Webhook URL: ") if ask_webhook == "y" else None
clear()

worker_name = input("Worker name: ") if ask_webhook == "y" else None
clear()

worker_count = int(input("Worker count (10-100): ") or "100")
clear()

proxy_url = input("Proxy URL: ")
clear()

ip = socket.gethostbyname(socket.gethostname())
pid = os.getpid()
cpu = platform.processor()


if worker_name:
    webhook = DiscordWebhook(url=webhook_url, username=worker_name)
else:
    worker_number = random.randint(1, 100)
    worker_name = f"Worker {worker_number}"
    webhook = DiscordWebhook(url=webhook_url, username=worker_name)

try:
    embed = DiscordEmbed(title=" ", color=0x5865f2)
    embed.add_embed_field(name="IP", value=f"{ip}", inline=True)
    embed.add_embed_field(name="PID", value=f"{pid}", inline=True)
    embed.add_embed_field(name="CPU", value=f"{cpu}", inline=False)
    embed.set_footer(text="By @rxyzqc")
    webhook.add_embed(embed)
    webhook.execute()
except:
    pass


chars = string.ascii_letters + string.digits

if not proxy_url:
    github_proxy_list_url = "https://raw.githubusercontent.com/rxyzqc/NitroGen/main/httpProxyURLS.txt"
    github_response = requests.get(github_proxy_list_url)
    github_proxy_list = github_response.text.strip().split("\n")
    selected_proxy_site = random.choice(github_proxy_list)
    selected_proxy_site = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all&simplified=true"

    proxy_response = requests.get(selected_proxy_site)
    proxy_list = proxy_response.text.strip().split("\n")
    proxies = [proxy.split()[0] for proxy in proxy_list]
    print(f"\033[32m[+]\033[0m {len(proxies)} proxies")
else:
    proxy_response = requests.get(proxy_url)
    proxy_list = proxy_response.text.strip().split("\n")
    proxies = [proxy.split()[0] for proxy in proxy_list]
    print(f"\033[32m[+]\033[0m {len(proxies)} proxies")

print('')

timeout_count = 0
invalid_count = 0
valid_count = 0

lock = threading.Lock()


def check_code(code, proxy):
    global timeout_count
    global invalid_count
    global valid_count

    code_url = api + code + api2
    proxy_url = f'http://{proxy}'

    proxy_config = {
        'http': proxy_url,
        'https': proxy_url
    }

    try:
        r = requests.get(code_url, proxies=proxy_config, timeout=10)
        rs = r.status_code

        if rs == 200:
            with lock:
                code_url = url + code
                print(f"\033[32mValid\033[0m   \033[34m|\033[0m {code} \033[34m|\033[0m {proxy}")
                with open("valid_codes.txt", "a") as f:
                    f.write(code_url + "\n")
                    f.close()

                try:
                    embed = DiscordEmbed(title=code, url=code_url, color=0x00ff00)
                    embed.set_author(name=worker_name)
                    embed.set_footer(text="By @rxyzqc")
                    webhook.add_embed(embed)
                    webhook.execute()
                except:
                    pass

                valid_count += 1
                update_title(
                    f"NitroGen By @rxyzqc ^| Timeout: {timeout_count} Invalid: {invalid_count} Valid: {valid_count}")

        elif rs == 404:
            print(f"\033[31mInvalid\033[0m \033[34m|\033[0m {code} \033[34m|\033[0m {proxy}")
            invalid_count += 1
            update_title(
                f"NitroGen By @rxyzqc ^| Timeout: {timeout_count} Invalid: {invalid_count} Valid: {valid_count}")

        elif rs == 429:
            print(f"\033[93mTimeout\033[0m \033[34m|\033[0m {code} \033[34m|\033[0m {proxy}")
        else:
            print(f"\033[35mError\033[0m \033[34m|\033[0m {code} \033[34m|\033[0m {proxy}")

    except requests.RequestException:
        # print(f"\033[93mTimeout\033[0m \033[34m|\033[0m {code} \033[34m|\033[0m {proxy}")
        timeout_count += 1
        update_title(f"NitroGen By @rxyzqc ^| Timeout: {timeout_count} Invalid: {invalid_count} Valid: {valid_count}")
        pass


def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=worker_count) as executor:
        while True:
            code = "".join(random.choice(chars) for _ in range(16))
            proxy = random.choice(proxies)
            executor.submit(check_code, code, proxy)


if __name__ == "__main__":
    main()
