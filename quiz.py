# quiz.py
"""
Cryptography Quiz System
Extensible quiz module for testing cipher knowledge
"""

import random
import math
from utils import GREEN, YELLOW, RED, GREY, RESET, clear_screen, center_text

# ============================================================================
# QUIZ QUESTION DATABASE
# ============================================================================
# Format: {
#   "cipher_name": [
#       {
#           "question": "Question text",
#           "options": ["A) option1", "B) option2", "C) option3", "D) option4"],
#           "correct": "A",  # or 0 for index-based
#           "explanation": "Why this is correct"
#       }
#   ]
# }

QUIZ_QUESTIONS = {
    "Caesar": [
        {
            "question": "What type of cipher is the Caesar cipher?",
            "options": [
                "A) Substitution cipher",
                "B) Transposition cipher",
                "C) Stream cipher",
                "D) Block cipher"
            ],
            "correct": "A",
            "explanation": "The Caesar cipher is a substitution cipher that replaces each letter with another letter a fixed number of positions down the alphabet."
        },
        {
            "question": "If you encrypt 'HELLO' with a Caesar shift of 3, what do you get?",
            "options": [
                "A) IFMMP",
                "B) KHOOR",
                "C) GDKKN",
                "D) LIPPS"
            ],
            "correct": "B",
            "explanation": "Each letter shifts 3 positions forward: H→K, E→H, L→O, L→O, O→R"
        },
        {
            "question": "How many possible keys does a Caesar cipher have?",
            "options": [
                "A) 13",
                "B) 25",
                "C) 26",
                "D) Infinite"
            ],
            "correct": "B",
            "explanation": "There are 25 meaningful shifts (1-25). A shift of 0 or 26 leaves the text unchanged."
        },
        {
            "question": "What is the main weakness of the Caesar cipher?",
            "options": [
                "A) It's too slow to encrypt",
                "B) It requires a very long key",
                "C) It can be broken by brute force easily",
                "D) It only works with lowercase letters"
            ],
            "correct": "C",
            "explanation": "With only 25 possible keys, all shifts can be tested in seconds to find the correct one."
        }
    ],
    
    "ROT13": [
        {
            "question": "What is special about ROT13?",
            "options": [
                "A) It uses a random shift",
                "B) Encrypting twice returns the original text",
                "C) It only works on vowels",
                "D) It requires a secret key"
            ],
            "correct": "B",
            "explanation": "ROT13 is its own inverse. Since it shifts by 13 (half the alphabet), applying it twice returns to the original text."
        },
        {
            "question": "ROT13 is a special case of which cipher?",
            "options": [
                "A) Vigenère",
                "B) Atbash",
                "C) Caesar",
                "D) Playfair"
            ],
            "correct": "C",
            "explanation": "ROT13 is simply a Caesar cipher with a fixed shift of 13."
        },
        {
            "question": "What is the primary use of ROT13 today?",
            "options": [
                "A) Military communications",
                "B) Banking security",
                "C) Obscuring spoilers and puzzles",
                "D) Government encryption"
            ],
            "correct": "C",
            "explanation": "ROT13 is not secure, but it's useful for hiding text that someone might not want to accidentally read, like spoilers."
        }
    ],
    
    "Atbash": [
        {
            "question": "How does the Atbash cipher work?",
            "options": [
                "A) It shifts letters by 13",
                "B) It reverses the alphabet (A↔Z, B↔Y, etc.)",
                "C) It uses a keyword",
                "D) It scrambles letter positions"
            ],
            "correct": "B",
            "explanation": "Atbash replaces each letter with its reverse in the alphabet: A becomes Z, B becomes Y, and so on."
        },
        {
            "question": "What language was Atbash originally used with?",
            "options": [
                "A) Latin",
                "B) Greek",
                "C) Hebrew",
                "D) Arabic"
            ],
            "correct": "C",
            "explanation": "Atbash is a Hebrew cipher. The name comes from the first, last, second, and second-to-last letters of the Hebrew alphabet."
        },
        {
            "question": "Like ROT13, what property does Atbash have?",
            "options": [
                "A) It's unbreakable",
                "B) It's self-inverse",
                "C) It requires two keys",
                "D) It only encrypts consonants"
            ],
            "correct": "B",
            "explanation": "Applying Atbash twice returns the original text because reversing the reverse gets you back to the start."
        }
    ],
    
    "Vigenère": [
        {
            "question": "What makes the Vigenère cipher stronger than Caesar?",
            "options": [
                "A) It uses multiple shift values",
                "B) It transposes letters",
                "C) It uses mathematical operations",
                "D) It requires special equipment"
            ],
            "correct": "A",
            "explanation": "Vigenère uses a keyword to determine different shift values for each letter, making frequency analysis harder."
        },
        {
            "question": "If the keyword is 'CAT' and plaintext is 'HELLO', what happens?",
            "options": [
                "A) All letters shift by 3",
                "B) H shifts by C(2), E by A(0), L by T(19), etc.",
                "C) The cipher fails",
                "D) Only vowels are encrypted"
            ],
            "correct": "B",
            "explanation": "Each letter of the keyword determines the shift for the corresponding plaintext letter, cycling through the keyword."
        },
        {
            "question": "What was the Vigenère cipher historically called?",
            "options": [
                "A) The Caesar Square",
                "B) Le Chiffre Indéchiffrable (The Indecipherable Cipher)",
                "C) The Perfect Cipher",
                "D) The Royal Code"
            ],
            "correct": "B",
            "explanation": "For centuries, Vigenère was considered unbreakable and was called 'The Indecipherable Cipher'."
        },
        {
            "question": "How can a Vigenère cipher be broken?",
            "options": [
                "A) It cannot be broken",
                "B) Frequency analysis after finding key length",
                "C) Only with the original keyword",
                "D) Using quantum computers"
            ],
            "correct": "B",
            "explanation": "The Kasiski examination can find the key length, then frequency analysis on each shift position can break the cipher."
        }
    ],
    
    "Beaufort": [
        {
            "question": "How does Beaufort differ from Vigenère?",
            "options": [
                "A) It uses subtraction instead of addition",
                "B) It only works with numbers",
                "C) It requires two keys",
                "D) It transposes instead of substitutes"
            ],
            "correct": "A",
            "explanation": "Beaufort uses (Key - Plaintext) mod 26 instead of (Plaintext + Key) mod 26 like Vigenère."
        },
        {
            "question": "What unique property does Beaufort have?",
            "options": [
                "A) It's unbreakable",
                "B) Encryption and decryption use the same operation",
                "C) It works without a key",
                "D) It only encrypts consonants"
            ],
            "correct": "B",
            "explanation": "Beaufort is reciprocal - you use the same process to encrypt and decrypt, just swap the ciphertext and plaintext positions."
        }
    ],
    
    "Autokey": [
        {
            "question": "What does the Autokey cipher use after the initial key?",
            "options": [
                "A) Random numbers",
                "B) The plaintext itself",
                "C) The alphabet in reverse",
                "D) Nothing - it stops"
            ],
            "correct": "B",
            "explanation": "After the initial primer/key, Autokey uses the plaintext itself as the continuing key, making it harder to break."
        },
        {
            "question": "Why is Autokey more secure than standard Vigenère?",
            "options": [
                "A) It uses longer keys",
                "B) The key doesn't repeat in a pattern",
                "C) It uses two alphabets",
                "D) It includes numbers"
            ],
            "correct": "B",
            "explanation": "Since the key is based on the plaintext, it doesn't repeat periodically, making Kasiski examination ineffective."
        }
    ],
    
    "Affine": [
        {
            "question": "The Affine cipher uses what type of mathematical operation?",
            "options": [
                "A) Addition only",
                "B) Multiplication only",
                "C) Both multiplication and addition",
                "D) Exponentiation"
            ],
            "correct": "C",
            "explanation": "Affine uses the formula (a*x + b) mod 26, combining multiplication and addition."
        },
        {
            "question": "Why must 'a' in the Affine cipher be coprime to 26?",
            "options": [
                "A) For faster computation",
                "B) To ensure the cipher is reversible",
                "C) To make it more secure",
                "D) It's just tradition"
            ],
            "correct": "B",
            "explanation": "If 'a' shares factors with 26, multiple plaintext letters could map to the same ciphertext letter, making decryption impossible."
        },
        {
            "question": "How many valid values can 'a' have in an Affine cipher?",
            "options": [
                "A) 12",
                "B) 13",
                "C) 25",
                "D) 26"
            ],
            "correct": "A",
            "explanation": "Only 12 numbers (1,3,5,7,9,11,15,17,19,21,23,25) are coprime to 26."
        }
    ],
    
    "Monoalphabetic Substitution Cipher": [
        {
            "question": "How many possible keys does a monoalphabetic substitution cipher have?",
            "options": [
                "A) 26",
                "B) 676",
                "C) 26! (factorial)",
                "D) Infinite"
            ],
            "correct": "C",
            "explanation": "There are 26! (about 4×10²⁶) possible ways to arrange the alphabet, making brute force impractical."
        },
        {
            "question": "What is the main weakness of monoalphabetic substitution?",
            "options": [
                "A) Too few possible keys",
                "B) Vulnerable to frequency analysis",
                "C) Requires long keys",
                "D) Can only encrypt short messages"
            ],
            "correct": "B",
            "explanation": "Each letter always maps to the same cipher letter, preserving letter frequencies and making frequency analysis effective."
        },
        {
            "question": "Which letter appears most frequently in English?",
            "options": [
                "A) A",
                "B) E",
                "C) T",
                "D) S"
            ],
            "correct": "B",
            "explanation": "The letter 'E' appears most frequently in English (~13%), making it a key target in frequency analysis."
        }
    ],
    
    "Rail Fence": [
        {
            "question": "What type of cipher is Rail Fence?",
            "options": [
                "A) Substitution",
                "B) Transposition",
                "C) Stream",
                "D) Block"
            ],
            "correct": "B",
            "explanation": "Rail Fence is a transposition cipher - it rearranges the order of letters without changing them."
        },
        {
            "question": "How does the Rail Fence cipher arrange text?",
            "options": [
                "A) In a square grid",
                "B) In a zigzag pattern across rows",
                "C) In reverse order",
                "D) In alphabetical order"
            ],
            "correct": "B",
            "explanation": "Letters are written in a zigzag pattern across multiple 'rails' (rows), then read off row by row."
        },
        {
            "question": "With 3 rails, where would the 5th character go?",
            "options": [
                "A) Rail 1",
                "B) Rail 2",
                "C) Rail 3",
                "D) Back to Rail 1"
            ],
            "correct": "A",
            "explanation": "The pattern zigzags: Rail 1→2→3→2→1, so the 5th character hits Rail 1 after bouncing back."
        }
    ],
    
    "Scytale": [
        {
            "question": "What ancient civilization used the Scytale?",
            "options": [
                "A) Romans",
                "B) Egyptians",
                "C) Spartans",
                "D) Vikings"
            ],
            "correct": "C",
            "explanation": "The Scytale was used by ancient Sparta for military communications as early as the 5th century BC."
        },
        {
            "question": "How was the Scytale cipher physically implemented?",
            "options": [
                "A) Using a code book",
                "B) Wrapping a strip around a rod",
                "C) Using special ink",
                "D) Rearranging wooden tiles"
            ],
            "correct": "B",
            "explanation": "A strip of leather or parchment was wrapped around a rod of specific diameter, and the message was written along the rod."
        },
        {
            "question": "What must the receiver have to decrypt a Scytale message?",
            "options": [
                "A) A code book",
                "B) A rod of the same diameter",
                "C) Special chemicals",
                "D) The original strip"
            ],
            "correct": "B",
            "explanation": "The receiver needs a rod of the exact same diameter to wrap the strip and read the message correctly."
        }
    ],
    
    "Columnar": [
        {
            "question": "How does a Columnar Transposition cipher work?",
            "options": [
                "A) Substitutes letters based on columns",
                "B) Writes text in rows, reads in column order based on key",
                "C) Only encrypts certain columns",
                "D) Shifts letters by column numbers"
            ],
            "correct": "B",
            "explanation": "Text is written in rows of a grid, then columns are read in an order determined by sorting the keyword."
        },
        {
            "question": "What determines the column reading order?",
            "options": [
                "A) The message length",
                "B) Alphabetical order of the keyword",
                "C) Random selection",
                "D) Left to right always"
            ],
            "correct": "B",
            "explanation": "The keyword's letters are sorted alphabetically, and columns are read in that sorted order."
        },
        {
            "question": "If the keyword is 'ZEBRA', which column is read first?",
            "options": [
                "A) Z (position 1)",
                "B) E (position 2)",
                "C) A (position 5)",
                "D) All columns simultaneously"
            ],
            "correct": "C",
            "explanation": "Columns are read in alphabetical order of the keyword, so A comes first, making position 5 first."
        }
    ],
    
    "Circular Bit Shift": [
        {
            "question": "What does a circular bit shift operate on?",
            "options": [
                "A) Letters only",
                "B) Binary representation of characters",
                "C) Word positions",
                "D) Alphabetical order"
            ],
            "correct": "B",
            "explanation": "Circular bit shift works on the binary (bit) representation of each character's ASCII value."
        },
        {
            "question": "What happens to bits that 'fall off' the end during a circular shift?",
            "options": [
                "A) They are lost",
                "B) They wrap around to the other end",
                "C) They become zeros",
                "D) They are saved for later"
            ],
            "correct": "B",
            "explanation": "In a circular shift, bits that move off one end reappear at the other end, preserving all information."
        },
        {
            "question": "How many bits are in a standard ASCII character?",
            "options": [
                "A) 4",
                "B) 8",
                "C) 16",
                "D) 32"
            ],
            "correct": "B",
            "explanation": "Standard ASCII uses 8 bits (1 byte) to represent each character, allowing 256 possible values."
        }
    ],
    
    "General Cryptography": [
        {
            "question": "What is the difference between encryption and encoding?",
            "options": [
                "A) They are the same thing",
                "B) Encryption requires a key, encoding doesn't",
                "C) Encoding is more secure",
                "D) Encryption is faster"
            ],
            "correct": "B",
            "explanation": "Encryption transforms data to hide it (requires a key), while encoding transforms data for compatibility (no key needed)."
        },
        {
            "question": "What is frequency analysis?",
            "options": [
                "A) Analyzing how often ciphers are used",
                "B) Counting letter occurrences to break substitution ciphers",
                "C) Measuring encryption speed",
                "D) Testing radio frequencies"
            ],
            "correct": "B",
            "explanation": "Frequency analysis exploits the fact that certain letters appear more often in language to break substitution ciphers."
        },
        {
            "question": "Which type of cipher is generally more secure?",
            "options": [
                "A) Substitution ciphers",
                "B) Transposition ciphers",
                "C) Combining both substitution and transposition",
                "D) Neither - they're equally secure"
            ],
            "correct": "C",
            "explanation": "Combining substitution and transposition creates stronger ciphers by defeating attacks on either method alone."
        },
        {
            "question": "What is a 'one-time pad'?",
            "options": [
                "A) A cipher that can only be used once",
                "B) A completely random key as long as the message",
                "C) A password written on paper",
                "D) An ancient encryption device"
            ],
            "correct": "B",
            "explanation": "A one-time pad uses a truly random key the same length as the message, used only once, making it theoretically unbreakable."
        },
        {
            "question": "What does 'cryptanalysis' mean?",
            "options": [
                "A) Creating new ciphers",
                "B) Breaking or analyzing ciphers",
                "C) Encoding messages",
                "D) Teaching cryptography"
            ],
            "correct": "B",
            "explanation": "Cryptanalysis is the study of analyzing and breaking codes and ciphers without knowing the key."
        }
    ]
}

# ============================================================================
# QUIZ LOGIC
# ============================================================================

def get_all_ciphers():
    """Returns list of all cipher topics"""
    return list(QUIZ_QUESTIONS.keys())

def get_questions_for_cipher(cipher_name):
    """Get all questions for a specific cipher"""
    return QUIZ_QUESTIONS.get(cipher_name, [])

def get_random_questions(num_questions=10, cipher_filter=None):
    """
    Get random questions from the quiz pool
    
    Args:
        num_questions: Number of questions to return
        cipher_filter: Optional list of cipher names to filter by
    
    Returns:
        List of question dictionaries with added 'cipher' key
    """
    all_questions = []
    
    ciphers_to_use = cipher_filter if cipher_filter else get_all_ciphers()
    
    for cipher in ciphers_to_use:
        questions = get_questions_for_cipher(cipher)
        for q in questions:
            q_copy = q.copy()
            q_copy['cipher'] = cipher
            all_questions.append(q_copy)
    
    if len(all_questions) <= num_questions:
        return all_questions
    
    return random.sample(all_questions, num_questions)

def normalize_answer(answer):
    """Normalize user input to match answer format"""
    answer = answer.strip().upper()
    # Accept full letter (A) or option format (A), A), etc.)
    if len(answer) >= 1:
        return answer[0]
    return answer

def run_quiz(num_questions=10, cipher_filter=None):
    """
    Run an interactive quiz
    
    Args:
        num_questions: Number of questions to ask
        cipher_filter: Optional list of cipher names to focus on
    
    Returns:
        dict with score statistics or None if user exits early
    """
    questions = get_random_questions(num_questions, cipher_filter)
    score = 0
    streak = 0
    total_points = 0
    results = []
    
    clear_screen()
    print(center_text("=" * 60))
    print(center_text("CRYPTOGRAPHY QUIZ"))
    print(center_text("=" * 60))
    print(center_text(f"Questions: {len(questions)}"))
    
    if cipher_filter:
        print(center_text(f"Topic: {', '.join(cipher_filter)}"))
    else:
        print(center_text("Topic: All Ciphers"))
    
    print(center_text("=" * 60))
    print(center_text(f"{YELLOW}(Type 'QUIT' or 'EXIT' at any time to return to menu){RESET}"))
    print(center_text("=" * 60))
    input(center_text("Press Enter to begin..."))
    
    for i, question in enumerate(questions, 1):
        clear_screen()
        print(center_text(f"Question {i}/{len(questions)}"))
        print(center_text(f"[{question['cipher']}]"))
        print(center_text("-" * 60))
        print()
        print(center_text(question['question']))
        print()
        
        for option in question['options']:
            print(center_text(option))
        
        print()
        print(f"{GREY}(Type QUIT or EXIT to return to menu){RESET}")
        user_answer = input("Your answer: " + " ").strip()
        
        # Check for exit commands
        if user_answer.upper() in ['QUIT', 'EXIT', 'Q']:
            clear_screen()
            print(center_text(f"{YELLOW}Quiz ended early{RESET}"))
            if i-1 == 0:
                print(center_text(f"{YELLOW}No questions answered yet{RESET}"))
            else:
                print(center_text(f"Questions answered: {i-1}/{len(questions)}"))
                print(center_text(f"Score so far: {score}/{i-1}"))
                print(center_text(f"Points earned: {total_points}"))
            print()
            input(center_text("Press Enter to return to menu..."))
            return None  # Return None to indicate early exit
        
        normalized = normalize_answer(user_answer)
        correct = question['correct']
        
        is_correct = normalized == correct
        
        # Calculate points with streak multiplier
        points_earned_this_question = 0
        if is_correct:
            streak += 1
            score += 1
            
            # Base points: 1 per correct answer
            base_points = 1.0
            
            # Apply multiplier if streak > 3
            if streak > 3:
                # Multiplier: 1.5x base, +0.5x per question after streak > 3
                multiplier = max(1.5, 1.0 + (streak - 3) * 0.5)
                points_earned_this_question = math.ceil(base_points * multiplier)
            else:
                points_earned_this_question = int(base_points)
            
            total_points += points_earned_this_question
        else:
            streak = 0  # Reset streak on incorrect answer
        
        print()
        if is_correct:
            if streak > 3:
                print(center_text(f"{GREEN}✓ Correct!{RESET} (+{points_earned_this_question} points, {streak} streak!)"))
            else:
                print(center_text(f"{GREEN}✓ Correct!{RESET} (+{points_earned_this_question} point)"))
        else:
            print(center_text(f"{RED}✗ Incorrect{RESET}"))
            print(center_text(f"The correct answer was: {GREEN}{correct}{RESET}"))
        
        print()
        print(center_text(f"{YELLOW}Explanation:{RESET}"))
        print(center_text(question['explanation']))
        print()
        
        results.append({
            'question': question['question'],
            'correct': is_correct,
            'user_answer': normalized,
            'correct_answer': correct,
            'points_earned': points_earned_this_question
        })
        
        if i < len(questions):
            input(center_text("Press Enter for next question..."))
    
    # Final results
    clear_screen()
    print(center_text("=" * 60))
    print(center_text("QUIZ COMPLETE"))
    print(center_text("=" * 60))
    
    percentage = (score / len(questions)) * 100
    
    print(center_text(f"Score: {score}/{len(questions)} ({percentage:.1f}%)"))
    print(center_text(f"Points Earned: {YELLOW}{total_points}{RESET}"))
    print()
    
    if percentage >= 90:
        grade = "Outstanding"
        color = GREEN
    elif percentage >= 75:
        grade = "Great Job"
        color = GREEN
    elif percentage >= 60:
        grade = "Good"
        color = YELLOW
    else:
        grade = "Keep Studying"
        color = RED
    
    print(center_text(f"{color}{grade}!{RESET}"))
    print(center_text("=" * 60))
    
    return {
        'score': score,
        'total': len(questions),
        'percentage': percentage,
        'points_earned': total_points,
        'results': results
    }

def quiz_menu():
    """Interactive menu for quiz system"""
    # Import storefront here to avoid circular import
    from main import run_storefront
    
    total_quiz_points = 0  # Accumulate points across quiz sessions
    
    while True:
        clear_screen()
        print(center_text("=" * 60))
        print(center_text("CRYPTOGRAPHY QUIZ"))
        print(center_text("=" * 60))
        print(center_text(f"Total Quiz Points: {YELLOW}{total_quiz_points}{RESET}"))
        print(center_text("=" * 60))
        print()
        print(center_text("Choose quiz mode:"))
        print()
        print(center_text("[1] Quick Quiz (10 questions - all topics)"))
        print(center_text("[2] Full Quiz (all questions - all topics)"))
        print(center_text("[3] Cipher-Specific Quiz"))
        print(center_text("[4] Custom Quiz"))
        print(center_text("[5] Visit Storefront"))
        print(center_text("[0] Back to Main Menu"))
        print()
        print(f"{GREY}(You can type QUIT or EXIT during any quiz to return here){RESET}")
        print()
        
        choice = input("Your choice: " + " ").strip()
        
        # Allow exit from menu selection too
        if choice.upper() in ['QUIT', 'EXIT', 'Q']:
            choice = "0"
        
        if choice == "0":
            break
        elif choice == "1":
            result = run_quiz(num_questions=10)
            if result is not None:  # Only show completion message if quiz finished
                total_quiz_points += result.get('points_earned', 0)
                input("\n" + center_text("Press Enter to continue..."))
        elif choice == "2":
            # Count all questions
            total = sum(len(q) for q in QUIZ_QUESTIONS.values())
            result = run_quiz(num_questions=total)
            if result is not None:
                total_quiz_points += result.get('points_earned', 0)
                input("\n" + center_text("Press Enter to continue..."))
        elif choice == "3":
            # Cipher-specific
            clear_screen()
            print(center_text("Select a cipher:"))
            print()
            ciphers = get_all_ciphers()
            for i, cipher in enumerate(ciphers, 1):
                num_q = len(get_questions_for_cipher(cipher))
                print(center_text(f"[{i}] {cipher} ({num_q} questions)"))
            print(center_text("[0] Back"))
            print()
            
            cipher_choice = input("Your choice: " + " ").strip()
            
            # Allow exit here too
            if cipher_choice.upper() in ['QUIT', 'EXIT', 'Q']:
                continue
            if cipher_choice == "0":
                continue
                
            try:
                idx = int(cipher_choice) - 1
                if 0 <= idx < len(ciphers):
                    selected_cipher = ciphers[idx]
                    questions = get_questions_for_cipher(selected_cipher)
                    result = run_quiz(num_questions=len(questions), cipher_filter=[selected_cipher])
                    if result is not None:
                        total_quiz_points += result.get('points_earned', 0)
                        input("\n" + center_text("Press Enter to continue..."))
            except ValueError:
                print(center_text(f"{RED}Invalid choice{RESET}"))
                input(center_text("Press Enter to continue..."))
        elif choice == "4":
            # Custom
            try:
                num_input = input("How many questions? " + " ").strip()
                
                # Allow exit here too
                if num_input.upper() in ['QUIT', 'EXIT', 'Q']:
                    continue
                    
                num = int(num_input)
                if num <= 0:
                    print(center_text(f"{RED}Please enter a positive number of questions.{RESET}"))
                    input(center_text("Press Enter to continue..."))
                    continue
                result = run_quiz(num_questions=num)
                if result is not None:
                    total_quiz_points += result.get('points_earned', 0)
                    input("\n" + center_text("Press Enter to continue..."))
            except ValueError:
                print(center_text(f"{RED}Invalid number{RESET}"))
                input(center_text("Press Enter to continue..."))
        elif choice == "5":
            # Visit Storefront
            if total_quiz_points > 0:
                run_storefront(total_quiz_points)
            else:
                print(center_text(f"{YELLOW}You need to earn points from quizzes first!{RESET}"))
                input(center_text("Press Enter to continue..."))

# ============================================================================
# TESTING & VALIDATION
# ============================================================================

def validate_quiz_data():
    """
    Validates the quiz question database for common errors
    Returns list of errors found
    """
    errors = []
    
    for cipher, questions in QUIZ_QUESTIONS.items():
        for i, q in enumerate(questions, 1):
            q_id = f"{cipher} Q{i}"
            
            # Check required fields
            if 'question' not in q:
                errors.append(f"{q_id}: Missing 'question' field")
            if 'options' not in q:
                errors.append(f"{q_id}: Missing 'options' field")
            if 'correct' not in q:
                errors.append(f"{q_id}: Missing 'correct' field")
            if 'explanation' not in q:
                errors.append(f"{q_id}: Missing 'explanation' field")
            
            # Check options format
            if 'options' in q:
                if len(q['options']) != 4:
                    errors.append(f"{q_id}: Should have exactly 4 options, has {len(q['options'])}")
                
                for opt in q['options']:
                    if not opt.startswith(('A)', 'B)', 'C)', 'D)')):
                        errors.append(f"{q_id}: Option doesn't start with A), B), C), or D): {opt}")
            
            # Check correct answer
            if 'correct' in q:
                if q['correct'] not in ['A', 'B', 'C', 'D']:
                    errors.append(f"{q_id}: Correct answer must be A, B, C, or D, got {q['correct']}")
    
    return errors

# ============================================================================
# TESTING & VALIDATION
# ============================================================================

def validate_quiz_data():
    """
    Validates the quiz question database for common errors
    Returns list of errors found
    """
    errors = []
    
    for cipher, questions in QUIZ_QUESTIONS.items():
        for i, q in enumerate(questions, 1):
            q_id = f"{cipher} Q{i}"
            
            # Check required fields
            if 'question' not in q:
                errors.append(f"{q_id}: Missing 'question' field")
            if 'options' not in q:
                errors.append(f"{q_id}: Missing 'options' field")
            if 'correct' not in q:
                errors.append(f"{q_id}: Missing 'correct' field")
            if 'explanation' not in q:
                errors.append(f"{q_id}: Missing 'explanation' field")
            
            # Check options format
            if 'options' in q:
                if len(q['options']) != 4:
                    errors.append(f"{q_id}: Should have exactly 4 options, has {len(q['options'])}")
                
                for opt in q['options']:
                    if not opt.startswith(('A)', 'B)', 'C)', 'D)')):
                        errors.append(f"{q_id}: Option doesn't start with A), B), C), or D): {opt}")
            
            # Check correct answer
            if 'correct' in q:
                if q['correct'] not in ['A', 'B', 'C', 'D']:
                    errors.append(f"{q_id}: Correct answer must be A, B, C, or D, got {q['correct']}")
    
    return errors

def run_quiz_tests():
    """Run validation tests on quiz data"""
    clear_screen()
    print(center_text("=" * 60))
    print(center_text("QUIZ DATA VALIDATION"))
    print(center_text("=" * 60))
    print()
    
    errors = validate_quiz_data()
    
    if not errors:
        print(center_text(f"{GREEN}✓ All quiz data is valid!{RESET}"))
        print()
        
        # Show statistics
        total_questions = sum(len(q) for q in QUIZ_QUESTIONS.values())
        print(center_text(f"Total ciphers: {len(QUIZ_QUESTIONS)}"))
        print(center_text(f"Total questions: {total_questions}"))
        print()
        
        print(center_text("Questions per cipher:"))
        for cipher, questions in sorted(QUIZ_QUESTIONS.items()):
            print(center_text(f"  {cipher}: {len(questions)}"))
    else:
        print(center_text(f"{RED}✗ Found {len(errors)} errors:{RESET}"))
        print()
        for error in errors:
            print(center_text(error))
    
    print()
    input(center_text("Press Enter to continue..."))

# ============================================================================
# EXAMPLE: Adding Your Own Questions
# ============================================================================

def add_custom_question(cipher_name, question_data):
    """
    Helper function to add a new question to the database
    
    Example usage:
        new_question = {
            "question": "What is your question?",
            "options": [
                "A) First option",
                "B) Second option",
                "C) Third option",
                "D) Fourth option"
            ],
            "correct": "A",
            "explanation": "Why this answer is correct"
        }
        add_custom_question("Caesar", new_question)
    """
    if cipher_name not in QUIZ_QUESTIONS:
        QUIZ_QUESTIONS[cipher_name] = []
    
    QUIZ_QUESTIONS[cipher_name].append(question_data)
    print(f"Added question to {cipher_name}")

# Main entry point
if __name__ == "__main__":
    # Run validation tests
    run_quiz_tests()