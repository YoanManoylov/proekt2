import random
import time
import json
from collections import deque

SCORE_FILE = "scores.json"


DIFFICULTIES = {
    "1": ("Лесно", 50, 10),
    "2": ("Средно", 100, 7),
    "3": ("Трудно", 200, 5)
}


def load_scores():
    try:
        with open(SCORE_FILE, "r") as f:
            return json.load(f)
    except:
        return {}


def save_scores(scores):
    try:
        with open(SCORE_FILE, "w") as f:
            json.dump(scores, f)
    except Exception as e: 
        print(f"\u26A0\uFE0F Грешка при запис: {e}")


def generate_hints(secret):
    hints = []
    hints.append(f"Числото е {'четно' if secret % 2 == 0 else 'нечетно'}.")
    digits_sum = sum(int(d) for d in str(secret))
    hints.append(f"Сумата на цифрите е {digits_sum}.")
    return hints

def choose_mode():
    print("\U0001F3AF Избери трудност:")
    for key, (name, max_points, attempts) in DIFFICULTIES.items():
        print(f"{key}. {name} (1-{max_points}, {attempts} опита)")

    while True:
        choice = input("Въведи 1, 2 или 3: ")

        if choice in DIFFICULTIES:
            _, max_points,attempts = DIFFICULTIES[choice]

            return max_points, attempts,choice


        print("\u26A0\uFE0F Грешен избор, пробвай пак!")


def play_game(max_number, max_attempts, start_time):
    secret = random.randint(1, max_number)
    attempts = 0
    history = []
    used = set()
    hints = generate_hints(secret)
    messages = deque(["Можеш! \U0001F4AA", "Не се отказвай! \U0001F680", "Почти си там! \U0001F3AF"])  # мотивиращи и нахъсващи съобщения ползвам опашка

    print(f"\nПознай число между 1 и {max_number}. Имаш {max_attempts} опита.")
    print("Команди: 'история', 'изход', 'подсказка'")

    while attempts < max_attempts:

        if time.time() - start_time > 300:
            print("\u23F0 Времето изтече!")
            return False, 0

        value = input("Въведи число: ").strip().lower()

        if value == "изход":
            print("\U0001F6AA Излезе от играта.")
            return False, 0
        if value == "история":
            print("\U0001F4DC Твоята история:", ", ".join(map(str, history)) or "няма")
            continue
        if value == "подсказка":
            if hints:
                print("\U0001F4A1 Подсказка:", hints.pop())
            else:
                print("\U0001F6AB Няма повече подсказки.")
            continue

        if not value.isdigit():
            print("\u26A0\uFE0F Въведи само число!")
            continue

        guess = int(value)
        if not (1 <= guess <= max_number):
            print(f"\u26A0\uFE0F Числото трябва да е между 1 и {max_number}.")
            continue

        if guess in used:

            print("\U0001F501 Вече си пробвал това число.")
            continue

        attempts += 1
        history.append(guess)
        used.add(guess)

        if guess < secret:
            print("\U0001F53C По-голямо!")
        elif guess > secret:
            print("\U0001F53D По-малко!")
        else:
            points = (max_attempts - attempts + 1) * 10
            print(f"\u2705 Позна! Опити: {attempts}. Точки: {points}")
            return True, points

        if messages:
            print(messages.popleft())

    print(f"\u274C Не успя. Числото беше {secret}.")
    return False, 0


def main():
    scores = load_scores()
    player = input("Въведи име: ").strip() or "Гост"
    player = player.title()

    max_number, max_attempts, diff_key = choose_mode()
    total = 0
    best = scores.get(player, 0)
    start = time.time()

    while True:
        win, points = play_game(max_number, max_attempts, start)
        total += points
        if total > best:
            best = total


        if not win or time.time() - start > 300:
            print(f"\n\U0001F3C1 Край, {player}! Точки: {total}")
            print(f"\U0001F3C6 Най-добър резултат: {best}")
            break


        max_number += 20
        if max_attempts > 3:
            max_attempts -= 1
        print(f"\n\U0001F680 Ниво нагоре! Нов диапазон: 1-{max_number}, опити: {max_attempts}")


    scores[player] = best
    save_scores(scores)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\U0001F6AA Играта спря.")