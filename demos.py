import time, string, shutil, re, os, sys, random
from utils import UP, RED, RESET, GREEN, YELLOW, GREY, FAST_CLEAR, FAST, get_terminal_width, center_text, clear_screen, ANSI_ESCAPE
from collections import OrderedDict
demo_registry = {}
def register_demo(name):
    def decorator(func):
        demo_registry[name] = func
        return func
    return decorator

@register_demo("Caesar")

def caesar_demo(word="hello", shift=3, delay=0.21):
    clear_screen()
    if shift is None:
        shift = random.randint(1, 25)

    bottom_row = ["." for _ in word]

    FRAME_LINES = 5

    # --- Initial Setup ---
    # Print the initial, static frame just once.
    print(center_text(f"Original word: {word}"))
    print(center_text(f"Shift amount: {shift}"))
    print() # Blank line
    print(center_text(" ".join(list(word))))
    print(center_text(" ".join(bottom_row)))
    
    time.sleep(1) # Pause before starting the animation
    
    for index, ch in enumerate(word):
        if not ch.isalpha():
            bottom_row[index] = ch
            continue # Skip animation for non-letters

        start = ord('a') if ch.islower() else ord('A')
        original_ord = ord(ch) - start

        # Animate the shift for the current letter
        for step in range(shift + 1):
            demo_ch = chr(start + ((original_ord + step) % 26))
            bottom_row[index] = demo_ch

            # --- Prepare the text for the two lines that change ---
            top_row_display = " ".join(
                f"{RED}{c}{RESET}" if j == index else c
                for j, c in enumerate(word)
            )
            bottom_row_display = " ".join(
                f"{RED}{c}{RESET}" if j == index else c
                for j, c in enumerate(bottom_row)
            )

            # --- Redraw only the changing lines ---
            sys.stdout.write(UP * 2) # Move cursor up 2 lines (to the top row)
            terminal_width = get_terminal_width()

            # Overwrite the old top and bottom rows
            sys.stdout.write(center_text(top_row_display).ljust(terminal_width) + "\n")
            sys.stdout.write(center_text(bottom_row_display).ljust(terminal_width) + "\n")
            
            sys.stdout.flush() # Force the update
            time.sleep(delay)

    # Move cursor to a new line after the animation is complete
    print("\n")
    print(center_text("Final Ciphertext: " + "".join(bottom_row)))

"""if __name__ == "__main__":
    print("This is a visual demonstration of how the Caesar cipher works. \n" \
    "Each letter is shifted by the same value, which is then used to decode the message by shifting each letter back by the same amount.")
    caesar_demo("helloworld", shift=5, delay=0.09)"""

@register_demo("Rot13")

def rot13_word_animation(word="helloworld"):
    clear_screen()
    shift = 13
    alphabet = list(string.ascii_lowercase)
    ciphered_display = [" " if c != " " else " " for c in word]

    last_frame_height = 0  # dynamically tracked

    def draw_frame(display_phrase, display_alphabet, display_cipher):
        nonlocal last_frame_height
        frame_lines = [
            center_text("ROT13 Demo: Letters move 13 slots through the alphabet"),
            center_text("Phrase : " + display_phrase),
            center_text("Alphabet: " + " ".join(display_alphabet)),
            center_text("Cipher  : " + " ".join(display_cipher))
        ]
        if last_frame_height:
            sys.stdout.write("\033[F" * last_frame_height)
        for line in frame_lines:
            sys.stdout.write("\033[2K")  # clear whole line regardless of width
            print(line)
        sys.stdout.flush()
        last_frame_height = len(frame_lines)


    # Print initial frame
    draw_frame(word, alphabet, ciphered_display)

    for idx, letter in enumerate(word):
        if not letter.isalpha():
            ciphered_display[idx] = letter
            draw_frame(word, alphabet, ciphered_display)
            continue

        current_index = alphabet.index(letter.lower())

        for step in range(1, shift + 1):
            display_alphabet = alphabet.copy()
            for s in range(step):
                trail_index = (current_index + s) % 26
                display_alphabet[trail_index] = f"{RED}{alphabet[trail_index]}{RESET}"

            moving_index = (current_index + step - 1) % 26
            display_alphabet[moving_index] = f"{RED}{alphabet[moving_index].upper()}{RESET}"

            display_phrase = "".join(
                (f"{RED}{c.upper()}{RESET}" if i == idx else c) for i, c in enumerate(word)
            )

            draw_frame(display_phrase, display_alphabet, ciphered_display)
            time.sleep(0.1)

        final_index = (current_index + shift) % 26
        ciphered_display[idx] = alphabet[final_index]

        display_alphabet = alphabet.copy()
        display_alphabet[final_index] = alphabet[final_index].upper()
        display_phrase = "".join(
            (c.upper() if i == idx else c) for i, c in enumerate(word)
        )

        draw_frame(display_phrase, display_alphabet, ciphered_display)
        time.sleep(0.15)

    print("\nFinal ciphered phrase:", "".join(ciphered_display))

@register_demo("Railfence")

def rail_fence_demo(word="HELLOWORLD", rails=3, delay=0.4):
    clear_screen()
    print(center_text("The rail fence cipher is a transposition cipher that writes characters in a zigzag pattern across a given number of rows(rails)."))

    header = f"Word: {word} | Rails: {rails}"
    print(center_text(header) + "\n")

    # Initialize rail structure
    fence = [["-" for _ in range(len(word))] for _ in range(rails)]

    # Print initial rails
    for row in fence:
        print(center_text(" ".join(row)))

    rail = 0
    direction = 1

    for col, ch in enumerate(word):
        # Place the letter in the correct rail
        fence[rail][col] = ch

        # Move cursor up to the start of rail lines
        sys.stdout.write(f"\033[{rails}F")  # move cursor up N lines
        # Print each rail line centered
        for row in fence:
            print(center_text(" ".join(row)))
        sys.stdout.flush()
        time.sleep(delay)

        # Move to next rail
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction *= -1

    # Build final ciphertext
    cipher = "".join(ch for row in fence for ch in row if ch != "-")
    print("\n" + center_text("Final Ciphertext: " + cipher))

"""

if __name__ == "__main__":
    rail_fence_demo("HELLOWORLD", rails=3, delay=0.4)
"""

#! VIGENERE
@register_demo("Vigenere")
def vigenere_number_animation(plaintext="HELLO WORLD", key="KEY", delay=0.8):
    """
    Animates Vigenère cipher with numeric values without clearing entire terminal.
    """
    clear_screen()
    def center_text(text):
        width = shutil.get_terminal_size().columns
        return text.center(width)

    plaintext = plaintext.upper()
    key = key.upper()
    key_len = len(key)
    ciphertext = ""

    # Initial display of plaintext and aligned key
    aligned_key = [key[i % key_len] for i in range(len(plaintext))]
    print(center_text("Phrase:     " + " ".join(plaintext)))
    print(center_text("Key:        " + " ".join(aligned_key)))
    print(center_text("Calculation:"))
    print(center_text("Ciphertext:"))

    for i, p_char in enumerate(plaintext):
        if not p_char.isalpha():
            ciphertext += p_char
            continue

        k_char = key[i % key_len]

        # Numeric values
        p_num = ord(p_char) - ord('A')
        k_num = ord(k_char) - ord('A')
        c_num = (p_num + k_num) % 26
        c_char = chr(c_num + ord('A'))
        ciphertext += c_char

        # Build highlighted plaintext and key
        plaintext_display = " ".join(
            f"{RED}{c}{RESET}" if j == i else c
            for j, c in enumerate(plaintext)
        )
        key_display = " ".join(
            f"{RED}{key[j % key_len]}{RESET}" if j == i else key[j % key_len]
            for j in range(len(plaintext))
        )

        # Move cursor up 4 lines to overwrite previous output
        sys.stdout.write(UP*4)

        print(center_text("Phrase:     " + plaintext_display))
        print(center_text("Key:        " + key_display))
        print(center_text(f"Calculation: {p_char}={p_num} + {k_char}={k_num} -> {c_num} = {c_char}"))
        print(center_text("Ciphertext: " + " ".join(ciphertext)))

        time.sleep(delay)

#vigenere_number_animation("HELLO WORLD", "KEY", delay=1)

@register_demo("Circularbitshift")

def circular_bit_shift_animation(value=178, shift=5, direction='left', delay=0.5):
    """
    Animates circular bit shifts for an 8-bit integer.
    The same bit is highlighted in red as it moves across positions.
    
    value: integer 0-255
    shift: number of positions to shift
    direction: 'left' or 'right'
    delay: seconds between steps
    """

        
    if not 0 <= value <= 255:
        raise ValueError("Value must be 0-255 (8-bit).")

    bits = list(f"{value:08b}")  # 8-bit binary
    clear_screen()

    print(center_text(f"Initial value: {value} -> {''.join(bits)}"))
    time.sleep(1.5)

    # Track the index of the bit we want to follow
    tracked_index = 0 if direction == 'left' else len(bits) - 1
    tracked_bit = bits[tracked_index]
    FRAME_LINES = 1
    for s in range(shift):
        sys.stdout.write(UP * FRAME_LINES)

        # Circular shift
        if direction == 'left':
            bit = bits.pop(0)
            bits.append(bit)
        else:  # right
            bit = bits.pop()
            bits.insert(0, bit)

        # Update tracked_index after shift
        if direction == 'left':
            tracked_index = (tracked_index - 1) % 8
        else:
            tracked_index = (tracked_index + 1) % 8

        # Build display with highlighted tracked bit
        bit_display = ""
        for i, b in enumerate(bits):
            if i == tracked_index:
                bit_display += f"{RED}{b}{RESET}"
            else:
                bit_display += b

        current_value = int(''.join(bits), 2)
        print(center_text(f"Shift {s+1}/{shift} ({direction}): {bit_display} -> {current_value}"))
        time.sleep(delay)

    print(center_text(f"Final value after {shift} circular {direction} shift: {current_value}"))
    time.sleep(1.99)

# Example usage:
#circular_bit_shift_animation(178, shift=5, direction='left', delay=0.9)
@register_demo("Columnar")

def columnar_demo():
    clear_screen()
    key = "KEY"
    plaintext = "HELLO_WORLD_"   # padded with underscores
    cols = len(key)
    rows = (len(plaintext) + cols - 1) // cols  # ceiling division
    grid = [[" " for _ in range(cols)] for _ in range(rows)]

    # Column order: 2 above col 0, 1 above col 1, 3 above col 2
    order = [2, 1, 3]

    def display(ciphertext="", highlight=None):
        """
        highlight: tuple (row, col) -> highlight the cell in red
        """
        os.system("cls" if os.name == "nt" else "clear")
        print("Columnar Transposition Cipher Demo\n")
        print(" K   E   Y")
        print(" 2   1   3")
        for r, row in enumerate(grid):
            line = []
            for c, x in enumerate(row):
                if highlight == (r, c):
                    line.append(f"[{RED}{x}{RESET}]")   # highlight in red
                else:
                    line.append(f"[{x}]")
            print(" ".join(line))
        print("\nCiphertext:", ciphertext)

    # Step 1: fill plaintext row by row
    for i, ch in enumerate(plaintext):
        r, c = divmod(i, cols)
        grid[r][c] = ch
        display()
        time.sleep(0.3)

    time.sleep(1)

    # Step 2: read ciphertext column by column in given order
    ciphertext = ""
    for col in sorted(range(cols), key=lambda x: order[x]):
        for row in range(rows):
            ciphertext += grid[row][col]
            display(ciphertext, highlight=(row, col))
            time.sleep(0.45)

    print("\nFinal Ciphertext:", ciphertext)






@register_demo("Jefferson Discs")
def jefferson_cipher_demo(plaintext="DECRYPTME", key_offset=6):
    """
    Part 1: Assembles the 'locked' cipher disks.
    Part 2: Animates the decryption by aligning the ciphertext.
    """
    clear_screen()
    # --- 1. This part does work behind scenes (Initialization) ---
    alphabet = string.ascii_uppercase
    plaintext = plaintext.upper()
    ciphertext = ""

    # Every column will travel this many steps.
    
    TRAVEL_DISTANCE = 6 
    # The total width to draw is the last letter's start position.
    max_draw_width = (len(plaintext) - 1) + TRAVEL_DISTANCE

    # Initialize columns
    columns = []
    for col_num, p_char in enumerate(plaintext):
        if p_char not in alphabet:
            p_char = " "
            p_idx = 0
        else:
            p_idx = alphabet.index(p_char)
            
        # --- Jefferson Cipher Logic ---
        # 1. Calculate the ciphertext character based on the offset
        c_idx = (p_idx + key_offset) % 26
        c_char = alphabet[c_idx]
        ciphertext += c_char
        
        # 2. Give the column a random starting spin
        random_start_idx = random.randint(0, 25)
        
        columns.append({
            "plaintext_char": p_char,
            "ciphertext_char": c_char,
            "target_idx": c_idx,            # The index of the ciphertext char
            "current_idx": random_start_idx,# The current "spun" index
            "target_pos": col_num,          # For horizontal slot-in
            "current_pos": col_num + TRAVEL_DISTANCE # <-- Start relative to target
        })
    
    # This variable tracks the height of the *previous* frame
    prev_frame_lines = 8 # Part 1's frame is 8 lines
    print("\n" * prev_frame_lines)

    # --- PART 1: HORIZONTAL SLOT-IN (Assemble Disks) ---
    
    for col_num, col_to_animate in enumerate(columns):
        while col_to_animate['current_pos'] >= col_to_animate['target_pos']:
            sys.stdout.write(UP * prev_frame_lines) 
            
            frame_buffer = []
            frame_buffer.append(center_text("Discs with letters are stuck together according to a given key."))
            frame_buffer.append("") 

            pos_map = {}
            for i in range(col_num):
                slotted_col = columns[i]
                pos_map[slotted_col['target_pos']] = slotted_col
            pos_map[col_to_animate['current_pos']] = col_to_animate

            # Draw the disks in their *current* (randomly spun) state
            for row_name in ["top", "middle", "bottom"]:
                row_text = f"{row_name.capitalize():<8}"
                # --- NEW: Use max_draw_width for the loop ---
                for i in range(max_draw_width + 1):
                    if i in pos_map:
                        col_data = pos_map[i]
                        idx = col_data['current_idx'] # Use current spun index
                        
                        # --- This is the cipher logic ---
                        if row_name == "top":
                            letter = alphabet[(idx - key_offset + 26) % 26] # Plaintext reveal
                        elif row_name == "middle":
                            letter = alphabet[idx] # Ciphertext align
                        else:
                            letter = alphabet[(idx + 1) % 26] # Filler for bottom
                        # ---
                        
                        is_active = (col_data == col_to_animate)
                        if is_active:
                            row_text += f"{RED}{letter}{RESET} "
                        else:
                            row_text += f"{letter} "
                    else:
                        row_text += "  "
                        
                frame_buffer.append(center_text(row_text))
            
            frame_buffer.append("")
            frame_buffer.append(center_text(f"Slotting disk {col_num+1}..."))
            frame_buffer.append("") 

            terminal_width = get_terminal_width()
            for line in frame_buffer:
                sys.stdout.write(line.ljust(terminal_width) + "\n")
            
            sys.stdout.flush() 
            time.sleep(0.08)

            col_to_animate['current_pos'] -= 1

    # --- END OF PART 1 ---

    # --- START OF PART 2: DECRYPTION (Aligning Ciphertext) ---
    
    time.sleep(1.5) 
    
    # Animate columns one at a time
    for col_num, col in enumerate(columns):
        
        # Spin until the 'middle' (current_idx) matches the 'target' (ciphertext_idx)
        while col['current_idx'] != col['target_idx']:
            current_frame_lines = 10 
            sys.stdout.write(UP * prev_frame_lines) 
            
            frame_buffer = []
            frame_buffer.append(center_text("Spin discs until ciphertext is found. The plaintext will align aswell."))
            frame_buffer.append("")

            for row_name in ["top", "middle", "bottom"]:
                row_text = f"{row_name.capitalize():<8}"
                for c_num, c in enumerate(columns):
                    idx = c['current_idx']
                    
                    # --- The Cipher Drawing Logic ---
                    if row_name == "top":
                        letter = alphabet[(idx - key_offset + 26) % 26] # Plaintext
                    elif row_name == "middle":
                        letter = alphabet[idx] # Ciphertext
                    else:
                        letter = alphabet[(idx + 1) % 26] # Filler
                    # ---
                        
                    if c_num == col_num:
                        row_text += f"{RED}{letter}{RESET} " # Active spinning column
                    elif c['current_idx'] == c['target_idx']:
                        # --- MODIFICATION ---
                        # This column is already aligned. Color-code its rows.
                        if row_name == "top":
                            row_text += f"{GREEN}{letter}{RESET} " # Show aligned plaintext as green
                        elif row_name == "middle":
                            row_text += f"{RED}{letter}{RESET} " # Show aligned ciphertext as red
                        else:
                            row_text += f"{letter} " # Bottom row default
                        # --- END MODIFICATION ---
                    else:
                        row_text += f"{letter} " # Unaligned column
                frame_buffer.append(center_text(row_text))
            
            frame_buffer.append("")
            # Show the target ciphertext we are spinning for
            frame_buffer.append(center_text(f"Plaintext: {GREEN}{''.join([c['plaintext_char'] for c in columns])}{RESET}"))
            frame_buffer.append(center_text(f"Ciphertext: {RED}{ciphertext}{RESET}"))
            frame_buffer.append("") 

            terminal_width = get_terminal_width()
            for line in frame_buffer:
                sys.stdout.write(line.ljust(terminal_width) + "\n")
            
            sys.stdout.flush() 
            time.sleep(0.05) # Faster spin
            
            prev_frame_lines = current_frame_lines

            # --- Shift column logic ---
            col['current_idx'] = (col['current_idx'] + 1) % 26

    # --- END OF PART 2 ---

    # Final display
    sys.stdout.write(UP * prev_frame_lines)
    frame_buffer = []
    frame_buffer.append(center_text("Decryption Complete!"))
    frame_buffer.append("")

    for row_name in ["top", "middle", "bottom"]:
        row_text = f"{row_name.capitalize():<8}"
        for c in columns:
            idx = c['target_idx'] # All are at target index now
            
            if row_name == "top":
                letter = alphabet[(idx - key_offset + 26) % 26]
                row_text += f"{GREEN}{letter}{RESET} " # Highlight plaintext
            elif row_name == "middle":
                letter = alphabet[idx]
                row_text += f"{RED}{letter}{RESET} " # Highlight ciphertext
            else:
                letter = alphabet[(idx + 1) % 26]
                row_text += f"{letter} "
        frame_buffer.append(center_text(row_text))
    
    frame_buffer.append("")
    frame_buffer.append(center_text(f"Plaintext:  {GREEN}{plaintext}{RESET}"))
    frame_buffer.append(center_text(f"Ciphertext: {RED}{ciphertext}{RESET}"))
    frame_buffer.append("") 
    
    terminal_width = get_terminal_width()
    for line in frame_buffer:
        sys.stdout.write(line.ljust(terminal_width) + "\n")
    
    sys.stdout.flush()






@register_demo("Playfair")
def playfair_interactive_demo(plaintext="CYBERHAWKS", keyword="MONARCHY"):
    """
    Complete Playfair cipher demonstration combining grid creation and encryption.
    """
    clear_screen()
    
    # ?=========================================================================
    # !--- PART 1: Grid Creation Animation ---
    # ?=========================================================================
    
    # *--- Step 1: Get and Process Keyword ---
    sys.stdout.write(center_text("The Playfair Cipher: Part 1 - Grid Creation") + "\n\n")
    sys.stdout.write(center_text(f"To use the playfair cipher, we must first build a 5x5 grid.") + "\n")
    sys.stdout.write(center_text(f"The grid is built using a keyword with these rules:") + "\n\n")
    sys.stdout.write(center_text(f"  1. The letter {RED}J{RESET} is treated as {GREEN}I{RESET} (to fit 26 letters in 25 squares).") + "\n")
    sys.stdout.write(center_text(f"  2. {RED}Duplicate{RESET} letters in the keyword are removed.") + "\n")
    sys.stdout.write(center_text(f"  3. The grid is filled in with keyword letters first. Then, the rest of the alphabet is filled in.") + "\n" +"\n")
    
    
    sys.stdout.write(center_text(f"The default keyword is {GREEN}{keyword}{RESET}.") + "\n" + "\n")
    sys.stdout.flush()
    
    user_keyword = input("Enter a keyword or press Enter to use default: ").strip().upper()
    if not user_keyword:
        user_keyword = keyword
        
    # Prepare key: uppercase, no spaces, unique letters, J -> I
    processed_key = "".join(OrderedDict.fromkeys(user_keyword.replace(" ", "").replace("J", "I")))
    
    # Prepare alphabet
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ" # No J
    remaining_chars = "".join([c for c in alphabet if c not in processed_key])
    
    full_sequence = processed_key + remaining_chars

    # --- Step 2: Animate the Grid Filling ---
    grid = [['' for _ in range(5)] for _ in range(5)]
    
    for i, char_to_add in enumerate(full_sequence):
        sys.stdout.write(FAST)
        sys.stdout.write(center_text("The Playfair Cipher: Part 1 - Grid Creation") + "\n\n")
        
        # Display the processed key and remaining alphabet
        # Highlight the character currently being added
        seq_display = ""
        for char in full_sequence:
            if char == char_to_add:
                seq_display += f"{RED}{char}{RESET}"
            elif char in processed_key:
                seq_display += f"{GREEN}{char}{RESET}"
            else:
                seq_display += f"{GREY}{char}{RESET}"

        sys.stdout.write(center_text(f"{GREEN}Keyword Chars{RESET} | {GREY}Remaining Alphabet{RESET}") + "\n")
        sys.stdout.write(center_text(seq_display) + "\n\n")

        # Place the new character in the grid
        r, c = divmod(i, 5)
        grid[r][c] = char_to_add
        
        # Display the grid as it's being built
        lines = []
        lines.append("┌───┬───┬───┬───┬───┐")
        for row_idx, row in enumerate(grid):
            line = "│"
            for col_idx, val in enumerate(row):
                char = val if val else ' '
                color = GREEN if val in processed_key else RESET
                if row_idx == r and col_idx == c:
                    color = RED # Highlight the newly added char
                line += f" {color}{char}{RESET} │"
            lines.append(line)
            if row_idx < 4:
                lines.append("├───┼───┼───┼───┼───┤")
        lines.append("└───┴───┴───┴───┴───┘")

        for line in lines:
            sys.stdout.write(center_text(line) + "\n")
            
        sys.stdout.write(FAST)
        time.sleep(0.08) # Animation delay

    # --- Final Display ---
    clear_screen()
    sys.stdout.write(center_text("Part 1 - Grid Creation") + "\n\n")
    sys.stdout.write(center_text("Grid construction complete!") + "\n\n")
    
    lines = []
    lines.append("┌───┬───┬───┬───┬───┐")
    for row in grid:
        line = "│"
        for val in row:
            color = GREEN if val in processed_key else RESET
            line += f" {color}{val}{RESET} │"
        lines.append(line)
        if row != grid[-1]:
            lines.append("├───┼───┼───┼───┼───┤")
    lines.append("└───┴───┴───┴───┴───┘")

    for line in lines:
        sys.stdout.write(center_text(line) + "\n")
    
    sys.stdout.write("\n\n")
    sys.stdout.flush()
    input(center_text("Press Enter to continue to Part 2 (Encryption)..."))
    
    # ?=========================================================================
    # !--- PART 2: Encryption Animation ---
    # ?=========================================================================
    
    def find_pos(ch):
        for r, row in enumerate(grid):
            for c, val in enumerate(row):
                if val == ch:
                    return r, c
        return None

    def display_grid(highlight=None):
        lines = []
        lines.append("┌───┬───┬───┬───┬───┐")
        for r, row in enumerate(grid):
            line = "│"
            for c, val in enumerate(row):
                if highlight and (r, c) in highlight:
                    line += f" {RED}{val}{RESET} │"
                else:
                    line += f" {val} │"
            lines.append(line)
            if r < 4:
                lines.append("├───┼───┼───┼───┼───┤")
        lines.append("└───┴───┴───┴───┴───┘")
        
        centered_lines = [center_text(l) for l in lines]
        return "\n".join(centered_lines)

    # ? -----------------------------------------------
    # !       --- Part 2 Tutorial Screen ---
    # ?-----------------------------------------------
    sys.stdout.write(FAST_CLEAR) 
    sys.stdout.write(center_text("The Playfair Cipher: Part 2 - Encryption") + "\n\n")
    sys.stdout.write(center_text("Now, we'll use the grid to encrypt a message.") + "\n")
    sys.stdout.write(center_text("The plaintext is first broken into pairs (digraphs).") + "\n\n")
    
    sys.stdout.write(center_text(f"  - If a pair has double letters (e.g., {GREEN}'LL'{RESET}), it becomes {GREEN}'LX'{RESET}.") + "\n")
    sys.stdout.write(center_text(f"  - If the message has an odd length, an {GREEN}'X'{RESET} is added at the end.") + "\n\n")
    
    sys.stdout.write(center_text("Then, each pair is encrypted using 3 rules:") + "\n")
    sys.stdout.write(center_text(f"  1. {YELLOW}Same Row{RESET}: Letters shift to the {YELLOW}Right{RESET}.") + "\n")
    sys.stdout.write(center_text(f"  2. {YELLOW}Same Column{RESET}: Letters shift {YELLOW}Down{RESET}.") + "\n")
    sys.stdout.write(center_text(f"  3. {YELLOW}Rectangle{RESET}: Letters {YELLOW}Swap Corners{RESET}.") + "\n\n")
    
    sys.stdout.write(center_text(f"Our plaintext will be: {GREEN}{plaintext.upper()}{RESET}") + "\n\n")
    sys.stdout.flush()
    input(center_text("Press Enter to begin the encryption..."))
    # --- End of tutorial screen ---


    # --- Plaintext & Digraph Prep ---
    plaintext = plaintext.upper().replace("J","I").replace(" ", "")
    
    digraphs = []
    i = 0
    while i < len(plaintext):
        a = plaintext[i]
        if i + 1 < len(plaintext):
            if plaintext[i+1] == a:
                b = 'X'
                i += 1
            else:
                b = plaintext[i+1]
                i += 2
        else:
            b = 'X'
            i += 1
        digraphs.append(a+b)

    # --- Main Animation Loop ---
    history = []
    dig_index = 0
    sub_step = 0

    while dig_index < len(digraphs):
        
        # --- 1. STATE CALCULATION ---
        pair = digraphs[dig_index]
        r1, c1 = find_pos(pair[0])
        r2, c2 = find_pos(pair[1])

        if r1 == r2:
            new_positions = [(r1, (c1+1)%5), (r2, (c2+1)%5)]
            rule = "Same Row -> Shift Right"
        elif c1 == c2:
            new_positions = [((r1+1)%5, c1), ((r2+1)%5, c2)]
            rule = "Same Column -> Shift Down"
        else:
            new_positions = [(r1, c2), (r2, c1)]
            rule = "Rectangle -> Swap Corners"

        # --- 2. UPDATE HISTORY (if on sub_step 1) ---
        cipher_pair = "".join([grid[r][c] for r, c in new_positions])
        if sub_step == 1:
            if len(history) <= dig_index:
                history.append((pair, cipher_pair))
        
        # --- 3. BUILD DYNAMIC DISPLAY STRINGS ---
        plaintext_display = ""
        for i, dig in enumerate(digraphs):
            if i == dig_index:
                plaintext_display += f" {GREEN}{dig}{RESET}" # Current
            elif i < dig_index:
                plaintext_display += f" {GREY}{dig}{RESET}" # Done
            else:
                plaintext_display += f" {dig}" # Future (default color)
        
        ciphertext_display = ""
        for i, (p, c) in enumerate(history):
            if i == dig_index:
                ciphertext_display += f" {RED}{c}{RESET}" # Current
            else:
                ciphertext_display += f" {GREY}{c}{RESET}" # Done

        # --- 4. RENDER FRAME ---
        sys.stdout.write(FAST_CLEAR)
        sys.stdout.write(center_text("The Playfair Cipher: Part 2 - Encryption") + "\n\n")

        if sub_step == 0:
            sys.stdout.write(display_grid(highlight=[(r1,c1),(r2,c2)]) + "\n\n")
        else:
            sys.stdout.write(display_grid(highlight=new_positions) + "\n\n")
        
        sys.stdout.write(center_text(f"Plaintext: {plaintext_display.strip()}") + "\n")
        sys.stdout.write(center_text(f"Ciphertext: {ciphertext_display.strip()}") + "\n\n")

        if sub_step == 0:
            sys.stdout.write(center_text(f"Step A: Finding {GREEN}{pair}{RESET}. Press Enter to see transformation.") + "\n")
            sys.stdout.write(center_text(" ") + "\n") # <-- Fix for frame height artifact
        else:
            sys.stdout.write(center_text(f"Rule: {YELLOW}{rule}{RESET} | {GREEN}{pair}{RESET} -> {RED}{cipher_pair}{RESET}") + "\n")
            sys.stdout.write(center_text("Step B: Transformation applied.") + "\n")
        
        sys.stdout.flush()

        # --- 5. GET INPUT & UPDATE STATE ---
        choice = input(f"\n[Enter/c] - Continue, [b] - Back, [q] - Quit: ").lower().strip()
        
        if choice in ("", "c"):
            if sub_step == 0:
                sub_step = 1
            else:
                sub_step = 0
                dig_index += 1
        elif choice == "b":
            if sub_step == 1:
                sub_step = 0
                if history and history[-1][0] == pair:
                    history.pop() 
            elif sub_step == 0 and dig_index > 0:
                dig_index -= 1
                sub_step = 1
                if history:
                    history.pop() 
        elif choice == "q":
            sys.stdout.write("\n" + center_text("Demo quit by user.") + "\n")
            return
            
    # --- Final Result ---
    final_ciphertext = "".join(f"{GREY}{c}{RESET}" for _, c in history)
    sys.stdout.write("\n" + center_text(f"Final Ciphertext: {final_ciphertext}") + "\n")
    sys.stdout.flush()
    


# Run demo
#playfair_interactive_demo("HELLO")

# Import the symmetric cipher demo from hashdemo.py
from hashdemo import mini_hash_demo
@register_demo("Scytale")
def run_full_scytale_animation(plaintext="ciphersarecool!", cols=5, sleep_time=0.2, pause_time=2.0):
    """
    Scytale demo function, requires plaintext and cols kwargs.
    """
    clear_screen()
    # =========================================================================
    # --- NESTED HELPER FUNCTIONS FOR DRAWING ---
    # These functions build a list of strings (frame_buffer) and write it
    # all at once with sys.stdout.write to prevent flickering.
    # =========================================================================

    def _draw_part1_frame(grid_state, full_text, current_index, num_rows, num_cols, width):
        """Draws Part 1: Writing Plaintext"""
        frame_buffer = [FAST_CLEAR] # Start with a screen clear and reset
        
        frame_buffer.append(center_text("--- Part 1: Writing the Message (Row by Row) ---", width))
        
        # 1. Draw the Top Input Phrase
        top_phrase = "Plaintext: "
        if current_index == -1: # Final state
            top_phrase += full_text
        else:
            top_phrase += (
                full_text[:current_index]
                + RED
                + full_text[current_index]
                + RESET
                + full_text[current_index + 1 :]
            )
        frame_buffer.append(center_text(top_phrase, width))
        frame_buffer.append("") # Newline

        # 2. Draw the Grid
        frame_buffer.append(center_text("--- Scytale Grid ---", width))
        highlight_r, highlight_c = (-1, -1) if current_index == -1 else (current_index // num_cols, current_index % num_cols)
        
        for r in range(num_rows):
            row_str = ""
            for c in range(num_cols):
                char = grid_state[r][c]
                if r == highlight_r and c == highlight_c:
                    row_str += f"[{RED}{char}{RESET}] "
                elif char == " ":
                    row_str += f"[{GREY}.{RESET}] "
                else:
                    row_str += f"[{char}] "
            frame_buffer.append(center_text(row_str.strip(), width))
        frame_buffer.append("") # Newline
        
        # Write the entire frame buffer to stdout at once
        sys.stdout.write("\n".join(frame_buffer))
        sys.stdout.flush()

    def _draw_part2_frame(grid_state, built_ciphertext, char_being_added, highlight_r, highlight_c, num_rows, num_cols, width):
        """Draws Part 2: Reading Ciphertext"""
        frame_buffer = [FAST_CLEAR]

        frame_buffer.append(center_text("Next, we read each letter column by column. This gives an encrypted message we can pass to others who know", width))
        frame_buffer.append("")

        # 1. Draw the Grid
        for r in range(num_rows):
            row_str = ""
            for c in range(num_cols):
                char = grid_state[r][c]
                if r == highlight_r and c == highlight_c:
                    row_str += f"[{RED}{char}{RESET}] "
                else:
                    row_str += f"[{char}] "
            frame_buffer.append(center_text(row_str.strip(), width))
        frame_buffer.append("")

        # 2. Draw the Ciphertext
        if char_being_added:
            display_text = f"Ciphertext: {built_ciphertext}{RED}{char_being_added}{RESET}"
        else:
            display_text = f"Ciphertext: {built_ciphertext}"
        frame_buffer.append(center_text(display_text, width))
        frame_buffer.append("")
        
        sys.stdout.write("\n".join(frame_buffer))
        sys.stdout.flush()

    def _draw_part3_frame(grid_state, ciphertext, current_index, num_rows, num_cols, width):
        """Draws Part 3: Writing Ciphertext (Decrypt)"""
        frame_buffer = [FAST_CLEAR]

        frame_buffer.append(center_text("--- Part 3: Decrypting (Writing by Column) ---", width))

        # 1. Draw the Top Ciphertext Phrase
        top_phrase = "Ciphertext: "
        if current_index == -1: # Final state
            top_phrase += ciphertext
        else:
            top_phrase += (
                ciphertext[:current_index]
                + RED
                + ciphertext[current_index]
                + RESET
                + ciphertext[current_index + 1 :]
            )
        frame_buffer.append(center_text(top_phrase, width))
        frame_buffer.append("")

        # 2. Draw the Grid
        frame_buffer.append(center_text("--- Decryption Grid ---", width))
        highlight_r, highlight_c = (-1, -1) if current_index == -1 else (current_index % num_rows, current_index // num_rows)
        
        for r in range(num_rows):
            row_str = ""
            for c in range(num_cols):
                char = grid_state[r][c]
                if r == highlight_r and c == highlight_c:
                    row_str += f"[{RED}{char}{RESET}] "
                elif char == " ":
                    row_str += f"[{GREY}.{RESET}] "
                else:
                    row_str += f"[{char}] "
            frame_buffer.append(center_text(row_str.strip(), width))
        frame_buffer.append("")
        
        sys.stdout.write("\n".join(frame_buffer))
        sys.stdout.flush()

    def _draw_part4_frame(grid_state, built_text, char_being_added, highlight_r, highlight_c, num_rows, num_cols, width):
        """Draws Part 4: Reading Original Text"""
        frame_buffer = [FAST_CLEAR]
        
        frame_buffer.append(center_text("--- Part 4: Reading the Original Message (Row by Row) ---", width))
        frame_buffer.append("")

        # 1. Draw the Grid
        for r in range(num_rows):
            row_str = ""
            for c in range(num_cols):
                char = grid_state[r][c]
                if r == highlight_r and c == highlight_c:
                    row_str += f"[{RED}{char}{RESET}] "
                else:
                    row_str += f"[{char}] "
            frame_buffer.append(center_text(row_str.strip(), width))
        frame_buffer.append("")

        # 2. Draw the Final Decrypted Text
        if char_being_added:
            display_text = f"Original Text: {built_text}{RED}{char_being_added}{RESET}"
        else:
            display_text = f"Original Text: {built_text}"
        frame_buffer.append(center_text(display_text, width))
        frame_buffer.append("")

        sys.stdout.write("\n".join(frame_buffer))
        sys.stdout.flush()

    # =========================================================================
    # --- MAIN ANIMATION LOGIC ---
    # =========================================================================

    try:
        # --- 1. Setup ---
        # Hide cursor
        sys.stdout.write("\033[?25l")
        
        width = get_terminal_width()
        text_len = len(plaintext)
        rows = (text_len + cols - 1) // cols
        padded_text = plaintext + "@" * ((rows * cols) - text_len)
        
        # --- Part 1: Write Rows (Encrypt) ---
        grid = [[" " for _ in range(cols)] for _ in range(rows)]
        for i in range(len(padded_text)):
            r, c = i // cols, i % cols
            grid[r][c] = padded_text[i]
            _draw_part1_frame(grid, padded_text, i, rows, cols, width)
            time.sleep(sleep_time)
        
        _draw_part1_frame(grid, padded_text, -1, rows, cols, width)
        sys.stdout.write(center_text("Part 1 Complete!", width) + "\n")
        sys.stdout.flush()
        time.sleep(pause_time)

        # --- Part 2: Read Cols (Encrypt) ---
        ciphertext = ""
        for c in range(cols):
            for r in range(rows):
                char_to_add = grid[r][c]
                _draw_part2_frame(grid, ciphertext, char_to_add, r, c, rows, cols, width)
                time.sleep(sleep_time)
                ciphertext += char_to_add
        
        _draw_part2_frame(grid, ciphertext, "", -1, -1, rows, cols, width)
        sys.stdout.write(center_text("Ciphertext Complete!", width) + "\n")
        sys.stdout.flush()
        time.sleep(pause_time)

        # --- Part 3: Write Cols (Decrypt) ---
        grid3 = [[" " for _ in range(cols)] for _ in range(rows)]
        for i in range(len(ciphertext)):
            r, c = i % rows, i // rows
            grid3[r][c] = ciphertext[i]
            _draw_part3_frame(grid3, ciphertext, i, rows, cols, width)
            time.sleep(sleep_time)
            
        _draw_part3_frame(grid3, ciphertext, -1, rows, cols, width)
        sys.stdout.write(center_text("Part 3 Complete! Grid is refilled.", width) + "\n")
        sys.stdout.flush()
        time.sleep(pause_time)

        # --- Part 4: Read Rows (Decrypt) ---
        original_text = ""
        for r in range(rows):
            for c in range(cols):
                char_to_add = grid3[r][c]
                _draw_part4_frame(grid3, original_text, char_to_add, r, c, rows, cols, width)
                time.sleep(sleep_time)
                original_text += char_to_add
        
        _draw_part4_frame(grid3, original_text, "", -1, -1, rows, cols, width)
        sys.stdout.write(center_text("Decryption Complete!", width) + "\n")
        sys.stdout.flush()

    except KeyboardInterrupt:
        sys.stdout.write("\nAnimation stopped.\n")
    finally:
        # ALWAYS restore the terminal
        # Show cursor, reset colors
        sys.stdout.write(RESET + "\033[?25h" + "\n")
        sys.stdout.flush()

@register_demo("Symmetric Cipher Demo") 
def symmetric_cipher_demo_wrapper():
    clear_screen()
    mini_hash_demo()