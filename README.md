# Computational Screening of Passive Radiative Cooling Rooftop Materials Under Four Saudi Arabian Climates

Ibdaa 2027 project (Materials Science). This repository replaces the first version of the project (July 2026); see `CHANGES.md` for every change and why it was made.

## What it does
For every hour of typical-year weather at four Saudi stations (Dhahran, Jeddah, Al Wajh, Al Baha), the model solves the steady-state energy balance of a passive, sky-facing rooftop surface and predicts its temperature relative to the air. Each material is described by its solar absorptance (alpha) and thermal emissivity (epsilon).

- **Energy balance:** grey-body radiation, clear sky, insulated back.
- **Sky emissivity:** Berdahl & Fromberg (1982) dew-point correlation.
- **Convection:** standard flat-plate correlations (Incropera et al.), with hourly station pressure.
- **Solver:** Brent's method (`scipy.optimize.brentq`), bracketed ±100 K around air temperature.

## Data
- **Weather:** Climate.OneBuilding TMYx files in `epw_files/` (Dhahran, Jeddah and Al Baha: 2011–2025 records; Al Wajh: 2007–2021).
- **Materials:** `materials_verified.csv` holds the 4 PDRC materials and 1 commercial white paint control whose properties were checked against the original papers (source page recorded for each). `materials_database.csv` is the older literature list; its values have **not** yet been verified.

## Validation status
**Not yet validated.** The first version reported a validation accuracy that could not be reproduced from its code, so it was removed (`reproduce_last_year.py` documents this). No published outdoor experiment found so far reports every condition the model needs without a wind shield. Validation is planned for November–December 2026. All results are model predictions.

The code itself is verified: `check_solver.py` compares the solver with the first version's on every hour of all four weather files.

## How to run
```
pip install -r requirements.txt
python analysis_summer.py      # results/ (all numbers in the Qalib)
python make_figures.py         # figures/
python check_solver.py         # solver verification
streamlit run app.py           # interactive tool
```
