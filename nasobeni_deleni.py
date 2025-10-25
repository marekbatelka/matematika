import random
import time
import json
from pathlib import Path

# ----------------------------------------------------------------------
MULT_MAX = 10          # faktory násobení (1‑10)
DIV_MAX = 10           # dělitel i výsledek dělení (1‑10)
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
    """Vytvoří seznam všech unikátních otázek a zamíchá jej."""
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
    """Jedinečný klíč pro slovník."""
    return f"{a // b}/{b}" if op == "/" else f"{a}*{b}"


def evaluate(a: int, b: int, op: str, answer: float) -> bool:
    correct = (a * b) if op == "*" else (a // b)
    return abs(answer - correct) < 1e-6


def ask_with_second_chance(a: int, b: int, op: str) -> tuple[bool, bool]:
    """
    Vrací (správně?, ukončit?).
    Ukončení zadáním **e** (dříve bylo k).
    """
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


def print_summary(data: dict) -> None:
    total = sum(v["tries"] for v in data.values())
    correct = sum(v["correct"] for v in data.values())
    avg_time = (sum(v["total_time"] for v in data.values()) / total) if total else 0.0

    # formát s pevnou šířkou 10 znaků (zarovnání vpravo)
    def fmt(num):
        return f"{num:>10}"

    print("\n=== Souhrnná statistika ===")
    print(f"{'Celkem otázek:':<20}{fmt(total)}")
    if total:
        success_pct = correct / total * 100
        print(f"{'Správně:':<20}{fmt(correct)} ({success_pct:5.1f} %)")
    else:
        print(f"{'Správně:':<20}{fmt(0)}")
    print(f"{'Průměrný čas:':<20}{fmt(f'{avg_time:.2f} s')}")
    print("=" * 30 + "\n")


def print_detailed_stats(data: dict) -> None:
    """Tabulka se všemi příklady seřazená podle průměrného času (sestupně)."""
    rows = []
    for k, v in data.items():
        a_str, b_str = k.split("*") if "*" in k else k.split("/")
        op = "*" if "*" in k else "/"
        tries = v["tries"]
        correct = v["correct"]
        success_pct = (correct / tries) * 100 if tries else 0.0
        avg_time = v["total_time"] / tries if tries else 0.0
        rows.append(
            {
                "example": f"{a_str} {op} {b_str}",
                "tries": tries,
                "correct": correct,
                "success": success_pct,
                "avg_time": avg_time,
            }
        )

    # seřadíme podle průměrného času sestupně
    rows.sort(key=lambda r: r["avg_time"], reverse=True)

    # výpis jako markdown‑tabulka
    print("\n### Detailní statistika (seřazeno podle průměrného času)\n")
    print("| Příklad | Pokusů |  ✅  |  %  | ~ čas |")
    print("|---------|--------|------|-----|-------|")
    for r in rows:
        print(
            f"| {r['example']:<7} | {r['tries']:<6} |  {r['correct']:<3} | "
            f"{r['success']:3.0f} | {r['avg_time']:3.0f} \t|"
        )
    print()


# ----------------------------------------------------------------------
if __name__ == "__main__":
    data = load_data()
    question_pool = build_question_pool()
    print("=== Procvičování velké násobilky (1‑10) ===")
    print("Zadej 'e' místo odpovědi pro ukončení a zobrazení souhrnu.\n")

    while True:
        if not question_pool:                 # pool vyčerpán → zamícháme znovu
            question_pool = build_question_pool()

        a, b, op = question_pool.pop()
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
            print_detailed_stats(data)
            break

    save_data(data)
    print("Statistiky uloženy do", DATA_FILE)
