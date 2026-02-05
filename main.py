"""
Author: jburn20
Program that teaches student cryptography
"""
from demos import demo_registry
import random, os, sys, string, time, subprocess
from ciphers import generate_round, choose_difficulty_for_level, CIPHERS, generate_specific_round
# Import the new helper functions and GREY color
from utils import GREEN, YELLOW, RED, GREY, RESET, clear_screen, center_text, get_terminal_width
from quiz import quiz_menu

# --- Dev toggles ---
DEV_SHOW_CIPHER = False  # Show cipher names during gameplay
DEV_MODE = False  # Enable dev menu for testing features

# --- DELETED the old hard-coded STORE_ITEMS dictionary ---


# --- NEW: Dynamic Storefront Builder ---
def build_storefront_items():
    """
    Scans the 'prizes' directory and builds the store item list.
    Defaults all .json files to 1 point.
    Applies manual prices from the MANUAL_PRICES dict.
    """
    
    # ?---
    # !--- EDIT THIS DICTIONARY TO MANUALLY SET 3 OR 5 POINT PRICES ---
    # ?---
    MANUAL_PRICES = {
        'prizes/linuxtype.json': 3,
        'prizes/game!.json': 3,
        'prizes/multibond.json': 3,
        'prizes/ramen.json': 3,
        'prizes/round.json': 3,
        'prizes/dance2.json': 3,
        'prizes/juggler.json': 3,
        'prizes/lookrighthere.json': 3,
        'prizes/peter.json': 3,
        'prizes/steezy.json': 3,
        'prizes/exasperated.json': 3,
        'prizes/lockin.json': 3,
        'prizes/shymariachi.json': 5,
        'prizes/nerd.json': 5,
        'prizes/squid.json': 5,
        'prizes/newhope.json': 5,
        'prizes/static.json': 5,
        'prizes/swtor.json': 5,
        'prizes/keyboard.json': 5,
        'prizes/roguedata.json': 5,

    }
    # !---
    # ?--- END OF MANUAL CONFIGURATION ---
    # !---

    store_items = {}
    item_key = 1  # Start item numbering at 1
    prizes_dir = 'prizes'
    
    # *Ensure prizes directory exists
    if not os.path.exists(prizes_dir):
        return {} # Return empty store if no prize folder

    # !--- Step 1: Add all 1-point default items ---
    try:
        all_files = sorted(os.listdir(prizes_dir))
    except FileNotFoundError:
        return {} # Again, return empty if path is invalid
        
    for filename in all_files:
        if filename.endswith('.json'):
            file_path = os.path.join(prizes_dir, filename).replace("\\", "/") # Normalize path
            
            # ONLY add as a 1-point item if it's NOT in the manual list
            if file_path not in MANUAL_PRICES:
                store_items[str(item_key)] = {
                    'name': file_path,
                    'cost': 1,
                    'file': file_path
                }
                item_key += 1
                
    # !--- Step 2: Add all manually-priced items ---
    # *This loop ensures they are added *after* the defaults, with correct keys
    for file_path, cost in sorted(MANUAL_PRICES.items()):
        # Check if the manually-priced file actually exists
        if os.path.exists(file_path):
            store_items[str(item_key)] = {
                'name': file_path,
                'cost': cost,
                'file': file_path
            }
            item_key += 1
        else:
            print(f"[Store Warning] Manual price set for missing file: {file_path}")

    return store_items
# !--- End of new function ---


def _diff_color(difficulty):
    if difficulty == "easy":
        return GREEN
    if difficulty == "medium":
        return YELLOW
    return RED

def _clean_word(text):
    # *Allow letters plus spaces only
    return "".join(ch for ch in text if ch.isalpha() or ch == " ")

def random_picker():
    with open(os.path.join(os.path.dirname(__file__), "wordlist.txt"), "r") as f:
        raw = [line.rstrip("\n") for line in f if line.strip()]
    words = [w for w in (_clean_word(x) for x in raw) if w]
    return random.choice(words)

def smart_word_picker(cipher_name):
    """Select appropriate word length based on cipher type."""
    with open(os.path.join(os.path.dirname(__file__), "wordlist.txt"), "r") as f:
        raw = [line.rstrip("\n") for line in f if line.strip()]
    words = [w for w in (_clean_word(x) for x in raw) if w]
    
    # *Categorize words by length
    word_lengths = [len(word.split()) for word in words]
    short_words = [w for w in words if len(w.split()) <= 3]
    medium_words = [w for w in words if 3 < len(w.split()) <= 4]
    long_words = [w for w in words if len(w.split()) > 4]
    
    # !Select based on cipher type
    if cipher_name in ["Columnar", "Affine", "Monoalphabetic Substitution Cipher"]:
        # *Hard ciphers - prefer longer phrases for better patterns
        if long_words:
            return random.choice(long_words)
        elif medium_words:
            return random.choice(medium_words)
        else:
            return random.choice(words)
    else:
        # Easy ciphers - work with any length
        return random.choice(words)


# !--- Storefront Function ---
def run_storefront(total_score):
    """
    Displays the post-game storefront UI.
    Allows the user to spend 'total_score' as currency to buy animations.
    """
    current_score = total_score
    
    # !--- MODIFIED: Build store items dynamically ---
    STORE_ITEMS = build_storefront_items()
    if not STORE_ITEMS:
        print(center_text(f"{RED}No items found in 'prizes' directory!{RESET}"))
        input(center_text("Press Enter to continue..."))
        return

    # *Sort items by cost for display
    sorted_items = sorted(STORE_ITEMS.items(), key=lambda item: int(item[0]))    
    print(sorted_items)
    watched = []
    while True:
        clear_screen()
        # --- Corrected Centered Headers ---
        print(center_text("=" * 60))
        print(center_text("THEATER"))
        print(center_text("=" * 60))
        print(center_text(f"Your Points: {YELLOW}{current_score}{RESET}"))
        print("\n")
        # !--- New Color Key ---
        print(center_text(f"Cost Key: {GREEN}1 Point{RESET} | {YELLOW}3 Points{RESET} | {RED}5 Points{RESET}"))
        print(center_text("-" * 45))
        print("\nAvailable Animations:\n")

        # *--- New Single-Column List ---
        for key, item in sorted_items:
            cost = item['cost']
            name = item['name']
            # *Determine color by cost
            if cost == 1:
                color = GREEN
            elif cost == 3:
                color = YELLOW
            else:
                color = RED
            
            # *Override color if unaffordable
            if current_score < cost:
                color = GREY
            if name in watched: 
                color = GREY
                
            display_text = f"{color}[{key}] {name} ({cost} pt){RESET}"
            print("    " + display_text) # Indent for clarity
        
        # --- Handle User Input (FIXED Centering) ---
        print("\n" * 2)
        
        # Print the prompt centered on its own line
        prompt_text = "Enter an item number to buy, or [Q] to quit:"
        print(prompt_text)
        
        # Center the input cursor/prompt on the next line
        cursor_prompt = "> "
        choice = input(cursor_prompt).strip().lower()

        if choice == 'q':
            break # Exit the storefront loop

        if choice in STORE_ITEMS:
            item = STORE_ITEMS[choice]
            if current_score >= item['cost']:
                watched.append(item['name'])
                # Purchase successful
                current_score -= item['cost']
                clear_screen()
                print(center_text(f"Purchased a ticket for {item['name']} at {item['cost']} point(s)!"))
                print(center_text(f"You have {current_score} points remaining."))
                input(center_text("\nPress Enter to watch your animation..."))
                
                # Run the prize animation
                try:
                    subprocess.run([sys.executable, "prize.py", item['file']])
                except Exception as e:
                    print(center_text(f"[!] Could not run prize animation: {e}"))
                    input(center_text("Press Enter to continue..."))
            
            else:
                # Not enough points
                print(center_text(f"{RED}Not enough points!{RESET} You need {item['cost']} but only have {current_score}."))
                time.sleep(2)
        else:
            # Invalid choice
            print(center_text(f"{RED}Invalid selection.{RESET} Please enter a number or 'Q'."))
            time.sleep(1.5)

    clear_screen()
    print(center_text("Thanks for visiting the theater!"))
# !--- End of Storefront Function ---


def run_level_progression(seed=None):
    if seed is not None:
        random.seed(seed)
    
    total_score = 0
    rounds_played = 0
    recent = []
    
    while True:  # Main game loop - user chooses when to quit
        # Show current stats and difficulty selection
        clear_screen()
        print(center_text("=" * 50))
        print(center_text("CRYPTOGRAPHY CHALLENGE"))
        print(center_text("=" * 50))
        print(center_text(f"Current Score: {total_score}"))
        print(center_text(f"Rounds Played: {rounds_played}"))
        print(center_text("=" * 50))
        print("\nChoose your difficulty:")
        print(f"[1] Easy   - 3 points")
        print(f"[2] Hard   - 5 points") 
        print(f"[0] Quit Game")
        if DEV_MODE:
            print(f"[D] Dev: Add points")
        print("=" * 50)
        
        choice = input("Select difficulty: ").strip()
        
        # Dev command: add points directly
        if DEV_MODE and choice.lower() == 'd':
            try:
                points = int(input("Enter points to add: "))
                rounds = int(input("Enter rounds to add (optional, default 0): ") or 0)
                total_score += points
                rounds_played += rounds
                print(f"\n[DEV] Added {points} points and {rounds} rounds")
                input("Press Enter to continue...")
                continue
            except ValueError:
                print("[DEV] Invalid input, cancelled")
                input("Press Enter to continue...")
                continue
        
        if choice == "0":
            clear_screen()
            # !--- Corrected Centered Headers ---
            print(center_text("=" * 60))
            print(center_text("GAME COMPLETE"))
            print(center_text("=" * 60))
            print(center_text(f"Final Score:      {total_score}"))
            print(center_text(f"Rounds Played:    {rounds_played}"))
            print(center_text("=" * 60))
            
            # !--- Call the Storefront ---
            print("\n" + center_text("You can now spend your points at the Theater!"))
            input(center_text("Press Enter to continue..."))
            
            # This function will now handle the entire post-game loop
            run_storefront(total_score)
            
            # --- End of new logic ---
            
            print("\nThanks for playing!")
            break # This exits the main game
            
        # Map choice to difficulty
        difficulty_map = {"1": "easy", "2": "hard"}
        if choice not in difficulty_map:
            print("Invalid choice! Please try again.")
            input("Press Enter to continue...")
            continue
            
        difficulty = difficulty_map[choice]
        base_points = 3 if difficulty == "easy" else 5
        
        # Generate round
        word = random_picker()
        rnd = generate_round(word, difficulty, recent)
        word = smart_word_picker(rnd['name'])
        rnd = generate_specific_round(word, rnd['name'])
        current_cipher_name = rnd['name']
        points = base_points
        hint_tier = 0  # 0=none, 1=type only, 2=type+params
        
        # Play the round
        while True:
            diff_col = _diff_color(difficulty)
            clear_screen()
            print(f"Difficulty: {diff_col}{difficulty.capitalize()}{RESET} ({base_points} points)")
            print(f"Current Score: {total_score} | This Round: {points}")
            if DEV_SHOW_CIPHER or hint_tier > 0:
                print(f"Cipher: {diff_col}{current_cipher_name}{RESET}")
                if hint_tier >= 2 and 'params' in rnd and rnd['params']:
                    pretty = []
                    for k, v in rnd['params'].items():
                        label = k.capitalize()
                        pretty.append(f"{label}: {v}")
                    print(" | ".join(pretty))
            print("CIPHER:", rnd['ciphertext'])

            # Always show help options
            print("[R] Regenerate (same cipher, new word) - 1 point")
            if hint_tier == 0:
                tier1_cost = -(-points // 2)  # Ceiling division for half points
                print(f"[H] Hint - Reveal cipher type - {tier1_cost} points")
            elif hint_tier == 1:
                tier2_cost = max(0, points - 1)
                print(f"[H] Hint - Reveal parameters - {tier2_cost} points (sets to 1)")

            ans = input("What is the word?\n").strip()
            normalized_ans = ans.replace(" ", "").upper()
            normalized_plain = rnd["plaintext"].replace(" ", "").upper()

            # Commands - always available
            if normalized_ans.lower() in ("r", "regenerate"):
                points = max(0, points - 1)
                word = smart_word_picker(current_cipher_name)
                rnd = generate_specific_round(word, current_cipher_name)
                continue
            if normalized_ans.lower() in ("h", "hint"):
                if hint_tier == 0:
                    hint_tier = 1
                    tier1_cost = -(-points // 2)
                    points = max(0, points - tier1_cost)
                    continue
                elif hint_tier == 1:
                    hint_tier = 2
                    points = 1
                    continue
            if ans.lower() == "pass":
                rounds_played += 1
                break

            if normalized_ans == normalized_plain:
                award = max(points, 0)
                print(f"You win! Awarded {award} points!")
                total_score += award
                rounds_played += 1
                break
            else:
                # ! This was their FIRST mistake
                if points > 2:
                    points = 2 # Set points to 1 for the last chance
                    print("Incorrect! You have one more chance...")
                    time.sleep(0.75)
                
                # ! This was their FINAL mistake 1
                else:
                    print(f"\nIncorrect! The correct answer was: {GREEN}{rnd['plaintext']}{RESET}")
                    print("You get 1 point for trying.")
                    total_score += 1 # Give the consolation point
                    rounds_played += 1
                    break 

        recent.append(current_cipher_name)
        input("\nPress Enter to continue...")

def get_cipher_params(name):
    """Get parameters for a specific cipher from user input."""
    params = {}
    if name == "Caesar":
        params["shift"] = int(input("shift (1-25): ") or 3)
    elif name == "Vigenere":
        params["key"] = input("key (A-Z): ").strip().upper() or "KEY"
    elif name == "Columnar":
        params["key"] = input("key (A-Z, length 3-5): ").strip().upper() or "KEY"
    elif name == "Affine":
        params["a"] = int(input("a (coprime to 26): ") or 5)
        params["b"] = int(input("b (0-25): ") or 8)
    elif name == "Monoalphabetic Substitution Cipher":
        print("Using fixed substitution alphabet: QWERTYUIOPASDFGHJKLZXCVBNM")
        params = {}
    elif name == "Rail Fence":
        params["rails"] = int(input("rails (2-5): ") or 3)
    elif name == "Circular Bit Shift":
        params["shift"] = int(input("shift (1-7): ") or 3)
        params["direction"] = (input("direction [left/right]: ") or "left").strip().lower()
    elif name == "Beaufort":
        params["key"] = input("key (A-Z): ").strip().upper() or "KEY"
    elif name == "Autokey":
        params["primer"] = input("primer (1-3 letters): ").strip().upper() or "KEY"
    elif name == "Scytale":
        params["diameter"] = int(input("diameter (3-5): ") or 3)
    # !ROT13, Atbash: no params needed
    return params

def run_cipher_tester():
    print("\nCipher Tester: Choose any cipher and test with your input.\n")
    names = list(CIPHERS.keys())
    for i, name in enumerate(names, 1):
        print(f"[{i}] {name} ({CIPHERS[name]['difficulty']})")
    print("[0] Back")
    choice = input("Select a cipher: ").strip()
    if choice == "0":
        return
    try:
        idx = int(choice) - 1
        name = names[idx]
    except Exception:
        print("Invalid choice.")
        return
    meta = CIPHERS[name]
    
    # !Ask if user wants to use smart word picker or enter their own
    use_smart = input("Use smart word picker for this cipher? [Y/n]: ").strip().lower()
    if use_smart in ("", "y", "yes"):
        plaintext = smart_word_picker(name)
        print(f"Selected phrase: {plaintext}")
    else:
        plaintext = input("Enter plaintext (letters and spaces): ").rstrip("\n")
    
    auto = input("Auto-generate parameters? [Y/n]: ").strip().lower()
    if auto in ("", "y", "yes"):
        params = meta["params"]()
    else:
        params = get_cipher_params(name)
    ciphertext = meta["encrypt"](plaintext, params)
    print("\nResult:")
    print("Cipher:", name)
    print("Plain :", plaintext)
    print("Params:", params)
    print("Cipher:", ciphertext)

def run_demos():
    while True:
        print("\nAvailable Demos:")
        for i, name in enumerate(demo_registry.keys(), 1):
            print(f"[{i}] {name}")
        print("[0] Quit")

        choice = input("Select a demo: ").strip()
        if choice == "0":
            print("Quitting game, goodbye.")
            sys.exit()

        try:
            choice = int(choice)
            demo_name = list(demo_registry.keys())[choice - 1]
            print(f"\n--- Running {demo_name} ---\n")

            try:
                demo_registry[demo_name]()  # Run the selected demo
            except Exception as e:
                print(f"Error while running {demo_name}: {e}")

            print("\n--- Demo finished ---\n")

        except (ValueError, IndexError):
            print("Invalid choice, please try again.")

def run_demo(file_name):
    # Execute the demo file
    path = os.path.join('demos', file_name)
    with open(path) as f:
        code = f.read()
        exec(code, globals())

def dev_test_prize_system():
    """Dev mode: Test the prize/star rating system"""
    clear_screen()
    # !--- Corrected Centered Headers ---
    print(center_text("=" * 60))
    print(center_text("DEV MODE - STOREFRONT TEST"))
    print(center_text("=" * 60))
    print()
    print("Test the storefront with a custom point value.\n")
    
    try:
        score = int(input("Enter points to test store with: ") or "10")
        print(f"\nLoading storefront with {score} points...")
        input("Press Enter to continue...")
        run_storefront(score) # Call the storefront directly
    except ValueError:
        print("Invalid input")
    
    input("\nPress Enter to continue...")
    
if __name__ == "__main__":
    try:
        menu_text = "Welcome to a Cryptography learning game. Enter [1] to test your decryption skills, [2] for demos, or [3] for cipher tester, [4] for quiz"
        if DEV_MODE:
            menu_text += ", or [9] for dev tests"
        menu_text += ".\n"
        
        userMode = int(input(menu_text))
        if userMode == 1:
            # Interactive difficulty selection with point bounties
            print("Challenge mode: Choose your difficulty and earn points!")
            run_level_progression()
        elif userMode == 2:
            while True:
                run_demos()
        elif userMode == 3:
            while True:
                run_cipher_tester()
                back = input("\nTest another? [Y/n]: ").strip().lower()
                if back in ("n", "no"):
                    break
        elif userMode == 4:
            # QUIZ ABOUT CIPHERS
            quiz_menu()
        elif userMode == 9 and DEV_MODE:
            dev_test_prize_system() # This now tests the storefront
        else:
            if userMode == 9 and not DEV_MODE:
                print("Dev mode is disabled. Set DEV_MODE = True in main.py to enable.")
            else:
                print("Invalid mode selected.")
                
        # TODO: Iterate with this format
        
    except KeyboardInterrupt:
        print("\nQuitting game, goodbye.")