# C.I.P.H.E.R. Project: Cryptography Learning Suite
A Cryptography Training Solution

## About

This project is an interactive, terminal-based application designed to teach cryptography concepts. It combines a "Challenge Mode" to test your decryption skills with a library of visual, step-by-step "Learning Demos" that explain how different ciphers work.

## Main Features

### 1. Gameplay (Challenge Mode)

Test your skills by decrypting messages and earning points.

* **Choose Your Difficulty:** Start a new round by selecting "Easy" (3 points) or "Hard" (5 points).
* **Solve the Puzzle:** You are given a `ciphertext` and must find the original plaintext.
* **Use Hints:** If you're stuck, you can spend points to get hints, such as revealing the cipher's type or its specific parameters (e.g., the shift value or key).
* **Regenerate:** You can also spend 1 point to "regenerate" the puzzle, which keeps the same cipher but gives you a new word to decrypt.
* **Earn Points:** Correct answers award points. After the game, you can spend your `total_score` in the Theater.
* **The Theater:** A post-game storefront where you can spend your earned points to purchase and watch various prize animations.

### 2. Learning Demos

Access a library of visual, animated demonstrations to learn how ciphers operate. These demos run in your terminal and provide a step-by-step breakdown of the encryption process.

Available demos include:
* Caesar
* Rot13
* Railfence
* Vigenere
* Circular Bit Shift
* Columnar
* Jefferson Discs
* Playfair
* Scytale
* Symmetric Cipher Demo

## Other Features

### Cipher Tester

A sandbox mode that lets you experiment with any of the implemented ciphers. You can:
* Select a specific cipher from the list.
* Provide your own plaintext or use a "smart word picker".
* Manually set the cipher parameters (like a key or shift) or have them auto-generated.
* Instantly see the resulting plaintext, parameters, and ciphertext.

## Installation

This project requires several external libraries for its interactive terminal interface, including `inquirerpy` and `prompt_toolkit`. You can install these dependencies using the Python package manager, `pip`:

```bash
pip install -r requirements.txt
```
If you are having still having trouble after installing with pip, try installing the packages to a venv:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
If you cannot get packages to work correctly, you can always download a version with no external dependencies:
```bash
git clone https://github.com/jburn20/cryptographylearningsuite.git
cd cryptographylearningsuite
git checkout 5e00d122002075183d15f8163a726a8ae06bf05a
```
