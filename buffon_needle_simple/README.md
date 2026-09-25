# Buffonova jehla

Simulace Buffonova experimentu pro krátkou jehlu (l ≤ t).

Pro každý se vygeneruje x ~ U(0, t/2) (vzdálenost středu jehly od nejbližší čáry) a θ ~ U(0, π/2) (úhel jehly s čarami).
Jehla protne čáru, když x ≤ (l/2)·sin θ.
Pravděpodobnost je P = 2l/(πt) => π ≈ 2lN/(tH), kde H je počet zásahů.

## Spuštění

    pip install -r requirements.txt
    python app.py

Pak otevřít http://127.0.0.1:5000, zadat N, l, t a Spustit.
