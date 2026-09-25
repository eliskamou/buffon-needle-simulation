# Buffonova jehla / Buffon's Needle

Interaktivní vizualizace Buffonovy úlohy o jehle – odhad čísla π házením jehel na linkovaný papír.
Interactive visualisation of Buffon's needle problem – estimating π by dropping needles on ruled paper.

## Spuštění / How to run

Otevřete `index.html` v libovolném moderním prohlížeči (Chrome, Edge, Firefox, Safari) – dvojklikem.
Nic se neinstaluje a nepotřebuje internet.

Just double-click `index.html`. No install, no server, no internet connection needed.
To move it to another PC, copy the folder (e.g. on a USB stick).

### Kiosk mode (for the event)

Full screen, no browser bars, no tabs to close by accident. Uses Chrome or Edge (falls back to the default browser).

| System | Start | Quit |
|---|---|---|
| Windows | double-click `start-windows.bat` | `Alt+F4` |
| macOS | double-click `start-mac.command` (first time: right-click → Open) | `Cmd+Q` |
| Linux | `./start-linux.sh` | `Alt+F4` |

If macOS says the file is not executable after copying: `chmod +x start-mac.command`.

## Ovládání / Controls

| | |
|---|---|
| Klik na papír / click paper | hodí jednu jehlu poblíž / drop one needle nearby |
| `Mezerník` / `Space` | start / pauza |
| `N` | jedna jehla / one needle |
| `R` | znovu / reset |
| `F` | celá obrazovka / fullscreen |
| `L` | čeština ↔ English |
| `S` | zvuk / sound on–off |

Parameters: needle length `l`, line spacing `t` (always `l ≤ t`), paper (A4 / A3 / full area), speed 1–5000 needles/s.
The chart card has two tabs: **Vývoj / Convergence** (estimate vs. N with the ±2σ band) and
**Opakování / Repeats** – 500 independent experiments with N = 100 / 1k / 10k needles, shown as histograms
of π̂ against the theoretical normal curve (σ ~ 1/√N).

Default language is set by `DEFAULT_LANG` at the top of the script in `index.html`.

## Model

- `x` – distance of the needle centre from the nearest line, `x ~ U(0, t/2)`
- `θ` – acute angle between needle and lines, `θ ~ U(0, π/2)`
- needle crosses a line ⇔ `x ≤ (l/2)·sin θ`, so `P = 2l / (πt)` and `π ≈ 2·l·N / (t·H)`

Paper size does not affect the result – only the ratio `l/t` does. The paper only has to be large enough
that every needle has a nearest line; in the app it only changes how the sheet looks.
