# Treasure Sprint (no pygame) - a fun choice-based adventure
import random
import time

def slow(text, d=0.02):
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(d)
    print()

def ask(prompt, options):
    options_lower = [o.lower() for o in options]
    while True:
        ans = input(prompt).strip().lower()
        if ans in options_lower:
            return ans
        slow(f"Choose: {', '.join(options)}")

def bar(value, maxv=10):
    filled = "█" * value
    empty = "░" * (maxv - value)
    return f"{filled}{empty} ({value}/{maxv})"

def main():
    random.seed()

    slow("🏁 WELCOME TO TREASURE SPRINT!")
    name = input("What's your name, runner? ").strip() or "Runner"
    slow(f"Alright {name}... Tonight, a treasure vault opens for 15 minutes.")
    slow("You must collect loot and escape. One problem: the maze is alive.\n")

    hp = 10
    stamina = 10
    coins = 0
    inventory = []
    turn = 0

    rooms = ["Hall", "Library", "Armory", "Garden", "Vault Door", "Tunnel", "Workshop", "Chamber"]
    special_items = ["rope", "torch", "lockpick", "bandage", "map"]
    boss_alive = True

    def status():
        slow(f"\n=== STATUS ===")
        slow(f"HP:      {bar(hp)}")
        slow(f"Stamina: {bar(stamina)}")
        slow(f"Coins:   {coins}")
        slow(f"Bag:     {', '.join(inventory) if inventory else '(empty)'}")
        slow("=============\n")

    slow("Tip: Pick smart actions. Stamina matters. Items help. Luck is real.\n")

    while True:
        turn += 1
        if hp <= 0:
            slow("💀 You collapse. The maze claims another challenger.")
            slow(f"Final coins: {coins}")
            break
        if stamina <= 0:
            slow("😵 You're exhausted and can barely move.")
            slow("You rest for a moment...")
            stamina = min(10, stamina + 4)

        room = random.choice(rooms)
        slow(f"📍 Turn {turn}: You enter the {room}.")

        # random events
        event_roll = random.random()

        if room == "Vault Door" and boss_alive:
            slow("🚪 The Vault Guardian appears! A metal statue with glowing eyes.")
            slow("It blocks the door to the treasure vault.")
            choice = ask("Do you (fight), (trick), or (run)? ", ["fight", "trick", "run"])

            if choice == "fight":
                stamina -= 2
                dmg = random.randint(1, 4)
                hit = random.randint(2, 5)
                slow(f"You strike hard! Guardian takes {hit} damage...")
                slow(f"It slams you back for {dmg} damage!")
                hp -= dmg
                if "torch" in inventory:
                    slow("🔥 Your torch blinds it—extra hit!")
                    hit += 2
                if hit >= 6:
                    slow("💥 The Guardian breaks apart! The vault path is open.")
                    boss_alive = False
                    coins += 15
                else:
                    slow("The Guardian is still active... it retreats into the shadows.")
            elif choice == "trick":
                stamina -= 1
                if "lockpick" in inventory or "map" in inventory:
                    slow("🧠 You use your tools and confuse its path logic.")
                    slow("✅ It freezes for a reboot. You slip past!")
                    boss_alive = False
                    coins += 10
                else:
                    slow("😬 You try to trick it, but it reads your move.")
                    dmg = random.randint(2, 4)
                    slow(f"It hits you for {dmg} damage!")
                    hp -= dmg
            else:  # run
                stamina -= 2
                slow("🏃 You run away, heart pounding.")
                coins = max(0, coins - 2)

        elif event_roll < 0.25:
            # loot
            found = random.randint(1, 6)
            stamina -= 1
            coins += found
            slow(f"💰 You find a stash! +{found} coins.")
            if random.random() < 0.35 and len(inventory) < 4:
                item = random.choice(special_items)
                if item not in inventory:
                    inventory.append(item)
                    slow(f"🎒 You also found a {item}!")
        elif event_roll < 0.50:
            # trap
            slow("🪤 Trap! The floor clicks under your foot.")
            stamina -= 1
            if "rope" in inventory and random.random() < 0.6:
                slow("🪢 You use your rope to swing to safety!")
            else:
                dmg = random.randint(1, 3)
                slow(f"💥 You get hurt: -{dmg} HP")
                hp -= dmg
        elif event_roll < 0.70:
            # puzzle
            slow("🧩 A puzzle door blocks your way.")
            a, b = random.randint(2, 9), random.randint(2, 9)
            ans = input(f"Solve to pass: {a} * {b} = ").strip()
            stamina -= 1
            if ans == str(a * b):
                slow("✅ Correct! You pass and grab coins behind it.")
                coins += 5
            else:
                slow("❌ Wrong! A dart hits you as you force it open.")
                hp -= 2
        elif event_roll < 0.88:
            # merchant
            slow("🧙 A sneaky merchant appears: 'Wanna trade?'")
            slow("1) Buy bandage (5 coins)  2) Buy torch (6 coins)  3) Leave")
            pick = ask("Choose 1/2/3: ", ["1", "2", "3"])
            if pick == "1" and coins >= 5:
                coins -= 5
                inventory.append("bandage")
                slow("✅ Bought bandage.")
            elif pick == "2" and coins >= 6:
                coins -= 6
                inventory.append("torch")
                slow("✅ Bought torch.")
            else:
                slow("You leave the merchant alone.")
        else:
            # rest spot
            slow("🛖 You find a quiet corner. You can rest or move on.")
            choice = ask("Do you (rest) or (move)? ", ["rest", "move"])
            if choice == "rest":
                stamina = min(10, stamina + 3)
                if "bandage" in inventory and hp < 10:
                    use = ask("Use bandage to heal? (yes/no): ", ["yes", "no"])
                    if use == "yes":
                        inventory.remove("bandage")
                        hp = min(10, hp + 3)
                        slow("🩹 Healed +3 HP.")
                slow("😌 Feeling better.")

        # win condition
        if not boss_alive and coins >= 30:
            slow("\n🏆 You reach the exit gate with enough treasure!")
            slow(f"🎉 CONGRATS {name}! You escaped with {coins} coins!")
            break

        # show status sometimes
        if turn % 3 == 0:
            status()

        # player choice to continue
        cont = ask("Continue? (y/n): ", ["y", "n"])
        if cont == "n":
            slow(f"👋 You quit safely with {coins} coins. See you next run!")
            break

if __name__ == "__main__":
    main()