# Grundlagen-Übung: Mini–Taschenrechner & Fehlersammlung

# 1) Werte und Typen
a = 7            # int
b = 2.5          # float
c = 3 + 4j       # complex
s = "Hallo"      # str

print("=== Werte und Typen ===")
print("a =", a, "| type:", type(a), "| id:", id(a))
print("b =", b, "| type:", type(b), "| id:", id(b))
print("c =", c, "| type:", type(c), "| id:", id(c))
print("s =", s, "| type:", type(s), "| id:", id(s))
print()

# 2) Grundrechenarten (mit int/float)
print("=== Grundrechenarten ===")
print("a + b =", a + b)
print("a - b =", a - b)
print("a * b =", a * b)
print("a / b =", a / b)    # echte Division (float)
print("a // 2 =", a // 2)  # Ganzzahl-Division
print("a % 2 =", a % 2)    # Modulo
print("a ** 3 =", a ** 3)  # Potenz
print()

# 3) Strings
print("=== Strings ===")
print('s + \" Welt\" =', s + " Welt")
print("s * 3 =", s * 3)
print()

# 4) Komplexe Zahlen
print("=== Komplexe Zahlen ===")
print("c =", c)
print("c.real =", c.real, "| c.imag =", c.imag)
print()

# 5) Bitoperationen (nur mit int sinnvoll)
x = 10  # 0b1010
y = 5   # 0b0101
print("=== Bitoperationen (int) ===")
print("x =", x, "y =", y)
print("~x =", ~x)         # Bitweises NOT
print("x & y =", x & y)   # AND
print("x | y =", x | y)   # OR
print("x ^ y =", x ^ y)   # XOR
print("x << 1 =", x << 1) # Links-Shift
print("x >> 1 =", x >> 1) # Rechts-Shift
print()

# 6) Funktionen print(), id(), type()
print("=== print, id, type ===")
print("print zeigt Werte:", a, b, c, s)
print("id(a) =", id(a))
print("type(b) =", type(b))
print()

# 7) Absichtlich Fehler provozieren (und sauber anzeigen)
def show_error(label, func):
    try:
        func()
    except Exception as e:
        print(f"[Fehler] {label}: {type(e).__name__}: {e}")

print("=== Fehler provozieren ===")
show_error("Division durch 0", lambda: 5/0)            # ZeroDivisionError
show_error("String + Zahl",   lambda: "Hallo" + 3)     # TypeError
show_error("Name nicht da",   lambda: print(x_undef))  # NameError
show_error("Ungültiger Shift",lambda: (1 << -1))       # ValueError (in neueren Pythons)
print()

print("Fertig. Du kannst das Script ändern und neu starten, um weiter zu experimentieren.")
