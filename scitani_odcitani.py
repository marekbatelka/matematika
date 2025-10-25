# bez zapornych cisel

import random

def get_valid_input(prompt):
    while True:
        user_input = input(prompt)
        if user_input.isdigit():  # Zkontrolujte, zda je vstup číslo
            return int(user_input)
        else:
            print("Prosím, zadej platné číslo.")

def main():
    max_value = get_valid_input("Do jaké hodnoty chceš procvičovat? ")  # Dotaz na maximální hodnotu
    correct_answers = 0  # Počet správných odpovědí
    total_questions = 0  # Celkový počet příkladů

    while True:
        total_questions += 1  # Zvyšte celkový počet otázek
        # Náhodně vybereme typ úlohy
        operation = random.choice(['+', '-'])  # Sčítání nebo odčítání
        
        if operation == '+':
            # Zajištění, že součet nebude větší než max_value
            a = random.randint(0, max_value)
            b = random.randint(0, max_value - a)  # Zajištění, že a + b <= max_value
            correct_answer = a + b
            user_answer = get_valid_input(f"VYPOČÍTEJ PŘÍKLAD: {a} + {b} = ")
        else:
            # Generování čísel pro odčítání
            a = random.randint(0, max_value)
            b = random.randint(0, a)  # Zajištění, aby b bylo menší nebo rovno a
            correct_answer = a - b
            user_answer = get_valid_input(f"VYPOČÍTEJ PŘÍKLAD: {a} - {b} = ")
        
        if user_answer == correct_answer:
            print("✅ SPRÁVNĚ :)")  # Zelený check
            correct_answers += 1  # Zvyšte počet správných odpovědí
        else:
            print("❌ ŠPATNĚ :(")  # Červený kříž
            print("ZKUS TO ZNOVA :(")

            # Další pokus
            user_answer = get_valid_input(f"VYPOČÍTEJ PŘÍKLAD: {a} {'+' if operation == '+' else '-'} {b} = ")
            
            if user_answer == correct_answer:
                print("✅ HURÁ NA PODRUHÉ SPRÁVNĚ :)")  # Zelený check
                correct_answers += 1  # Zvyšte počet správných odpovědí
            else:
                print("❌ ŠPATNĚ :(")  # Červený kříž

        # Zobrazte skóre jako správně / celkem
        print(f"Tvoje aktuální skóre: {correct_answers} / {total_questions}")

if __name__ == "__main__":
    main()
