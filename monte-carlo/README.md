# Monte Carlo: π z náhodných bodů / π from random points

Interaktivní vizualizace metody Monte Carlo: náhodné body ve čtverci ⟨−1, 1⟩ × ⟨−1, 1⟩ a vepsaný kruh o poloměru 1.
Interactive visualisation of the Monte Carlo method: random points in the square [−1, 1]² with an inscribed unit circle.

## Spuštění / How to run

Double-click `index.html` – no install, no server, no internet needed. Copy the whole folder to move it to another PC.

### Kiosk mode (for the event)

| System | Start | Quit |
|---|---|---|
| Windows | double-click `start-windows.bat` | `Alt+F4` |
| macOS | double-click `start-mac.command` (first time: right-click → Open) | `Cmd+Q` |
| Linux | `./start-linux.sh` | `Alt+F4` |

If macOS says the file is not executable after copying: `chmod +x start-mac.command`.

## Ovládání / Controls

| | |
|---|---|
| Klik na terč / click the target | hodí jeden náhodný bod / throw one random point |
| `Mezerník` / `Space` | start / pauza |
| `N` | jeden bod / one point |
| `R` | znovu / reset |
| `G` | přepne generátor / cycle the point generator |
| `F` | celá obrazovka / fullscreen |
| `L` | čeština ↔ English |
| `S` | zvuk / sound on–off |

Point generators:
- **Náhodné / Random** – `Math.random`, error ~ 1/√N.
- **Halton** – quasi-random sequence (bases 2 and 3, random shift), error ~ N^(−3/4) here (sharp circle edge).
- **Špatné LCG / Bad LCG** – `x = (5·x + 1) mod 2048`; points fall on lines and the estimate gets stuck at ≈ 3.207.

Chart tabs: **Vývoj / Estimate** (with ±2σ band), **Chyba / Error** (log–log with 1/√N and N^(−3/4) reference lines),
**Opakování / Repeats** (500 independent experiments with N = 100 / 1k / 10k, using the selected generator).

Default language is set by `DEFAULT_LANG` at the top of the script in `index.html`.

## Model

- point (x, y) with x, y ~ U(−1, 1) independent
- inside the circle ⇔ x² + y² ≤ 1, so P = π·1² / 2² = π/4 and `π ≈ 4·K / N`
- standard deviation of the estimate: 4·√(p(1−p)/N) ≈ 1.64/√N
