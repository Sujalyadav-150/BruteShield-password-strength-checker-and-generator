from flask import Flask, render_template, request
import hashlib
import re
import random
import string

app = Flask(__name__)

# Password Strength Checker
def check_strength(password):
    length = len(password)
    score = 0

    if length >= 8:
        score += 25
    if re.search(r"[a-z]", password):
        score += 15
    if re.search(r"[A-Z]", password):
        score += 20
    if re.search(r"\d", password):
        score += 20
    if re.search(r"\W", password):
        score += 20

    return min(score, 100)

# Password Hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Strong Password Generator
def generate_strong_password(length=14):
    characters = (
        string.ascii_letters +
        string.digits +
        string.punctuation
    )

    password = ''.join(random.choice(characters) for _ in range(length))
    return password

@app.route("/", methods=["GET", "POST"])
def index():
    hashed = ''
    decoded = ''
    strength = 0
    suggestion = ''

    if request.method == "POST":

        # Clear Button
        if "clear" in request.form:
            return render_template(
                "index.html",
                hashed='',
                decoded='',
                strength=0,
                suggestion=''
            )

        # Suggest Strong Password
        if "suggest" in request.form:
            password = generate_strong_password()
            suggestion = password
        else:
            password = request.form["password"]

        # Process Password
        strength = check_strength(password)
        hashed = hash_password(password)
        decoded = password

        # Store Strong Passwords
        if strength >= 70:
            with open("passwords.txt", "a") as file:
                file.write(
                    f"Decoded: {decoded}\n"
                    f"Encoded: {hashed}\n\n"
                )

    return render_template(
        "index.html",
        hashed=hashed,
        decoded=decoded,
        strength=strength,
        suggestion=suggestion
    )

if __name__ == "__main__":
    app.run(debug=True)