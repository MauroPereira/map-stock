from time import sleep

longitud = 40
percen = 0
linea = ("🚧") * (longitud + 3)
print(f"la barra del kpi\n{linea}\n")
for i in range(longitud):
    cuadra = "💹" * (i)
    espacio = "🟥" * (longitud - (i))
    percen = (i * 100) / longitud
    print(
        f"\r{percen}%[{cuadra}{espacio}]{i}/{longitud}", end="\r", flush=True
    )
    sleep(0.1)
cuadra = ("💹") * longitud
print(f"\r100%[{cuadra}] Download Complete!!!")
print(f"\n{linea}\n")
