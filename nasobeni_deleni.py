import random
import time
import json
from pathlib import Path

# ----------------------------------------------------------------------
MULT_MAX = 10          # faktory násobení
DIV_MAX   = 10         # dělitel i výsledek dělení
DATA_FILE = Path("procvicovani_data.json")
# ----------------------------------------------------------------------


def load_data() -> dict:
    if DATA_FILE.exists():
        with DATA_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_data(data: dict) -> None:
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def build_question_pool() -> list[tuple[int, int, str]]:
    """Vytvoří seznam všech unikátních otázek."""
    pool = []
    # násobení
    for a in range(1, MULT_MAX + 1):
        for b in range(1, MULT_MAX + 1):
            pool.append((a, b, "*"))
    # dělení – výsledek 1‑10, dělitel 1‑10
    for divisor in range(1, DIV_MAX + 1):
        for quotient in range(1, DIV_MAX + 1):
            dividend = divisor * quotient
            pool.append((dividend, divisor, "/"))
    random.shuffle(pool)
    return pool


def key(a: int, b: int, op: str) -> str:
    return f"{a // b}/{b}" if op == "/" else f"{a}*{b}"


def evaluate(a: int, b: int, op: str, answer: float) -> bool:
    correct = (a * b) if op == "*" else (a // b)
    return abs(answer - correct) < 1e-6


def ask_with_second_chance(a: int, b: int, op: str) -> tuple[bool, bool]:
    """Vrací (správně?, ukončit?). 'e' ukončí program."""
    correct_val = (a * b) if op == "*" else (a // b)

    raw = input(f"{a} {op} {b} = ").strip()
    if raw.lower() == "e":
        return False, True
    try:
        first = float(raw)
    except ValueError:
        print("❌ Neplatná odpověď.")
        first = None

    if first is not None and evaluate(a, b, op, first):
        print("✅ Správně!")
        return True, False

    print("❌ Špatně. Zkus to ještě jednou.")
    raw = input(f"{a} {op} {b} = ").strip()
    if raw.lower() == "e":
        return False, True
    try:
        second = float(raw)
    except ValueError:
        print("❌ Neplatná odpověď.")
        second = None

    if second is not None and evaluate(a, b, op, second):
        print("✅ Správně po druhé šanci!")
        return True, False

    print(f"❌ Špatně i podruhé. Správná odpověď je {correct_val}.")
    return False, False


def print_summary(data: dict):
    total = sum(v["tries"] for v in data.values())
    correct = sum(v["correct"] for v in data.values())
    avg_time = (sum(v["total_time"] for v in data.values()) / total) if total else 0.0
    print("\n=== Souhrnná statistika ===")
    print(f"Celkem otázek: {total}")
    if total:
        print(f"Správně: {correct} ({correct/total*100:.1f}% úspěšnost)")
    else:
        print("Správně: 0")
    print(f"Průměrný čas na otázku: {avg_time:.2f} s")
    if data:
        worst = sorted(
            data.items(),
            key=lambda kv: (kv[1]["correct"] / kv[1]["tries"], kv[1]["total_time"] / kv[1]["tries"]),
        )[0]
        a_str, b_str = worst[0].split("*") if "*" in worst[0] else worst[0].split("/")
        op = "*" if "*" in worst[0] else "/"
        print(f"Nejvíce chybovaný příklad: {a_str} {op} {b_str}")
    print("============================\n")


# ----------------------------------------------------------------------
if __name__ == "__main__":
    data = load_data()
    question_pool = build_question_pool()
    print("=== Procvičování velké násobilky (1‑10) ===")
    print("Zadej 'e' místo odpovědi pro ukončení a zobrazení souhrnu.\n")

    while True:
        if not question_pool:                 # pool vyčerpán → zamícháme znovu
            question_pool = build_question_pool()

        a, b, op = question_pool.pop()        # vezmeme poslední (náhodný) prvek
        start = time.time()
        correct, quit_flag = ask_with_second_chance(a, b, op)
        elapsed = time.time() - start

        k = key(a, b, op)
        stats = data.setdefault(k, {"tries": 0, "correct": 0, "total_time": 0.0})
        stats["tries"] += 1
        if correct:
            stats["correct"] += 1
        stats["total_time"] += elapsed

        if quit_flag:
            print_summary(data)
            break

    save_data(data)
    print("Statistiky uloženy do", DATA_FILE)
