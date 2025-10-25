import random

def main():
    score = 0  # Inicializace skóre

    while True:
        a = random.randint(0, 10)
        b = random.randint(0, 10)

        user_answer = int(input(f"VYPOČÍTEJ PŘÍKLAD: {a} + {b} = "))
        
        if user_answer == a + b:
            print("SPRÁVNĚ :)")
            score += 1  # Zvyšte skóre při správné odpovědi
        else:
            print("ŠPATNĚ :(")
            print("ZKUS TO ZNOVA :(")
            user_answer = int(input(f"VYPOČÍTEJ PŘÍKLAD: {a} + {b} = "))
            
            if user_answer == a + b:
                print("HURÁ NA PODRUHÉ SPRÁVNĚ :)")
                score += 1  # Zvyšte skóre za druhou správnou odpověď
            else:
                print("ŠPATNĚ :(")

        print(f"Tvoje aktuální skóre: {score}")

if __name__ == "__main__":
    main()
