from analyzer import analyze_code

code = """
def calculate_total(price, tax):
    total = price + (price * tax)

    if total > 100:
        print("Expensive")

    return total


price = 100
tax = 0.18

result = calculate_total(price, tax)

for i in range(3):
    print(result)
"""

result = analyze_code(code)

print(result)