import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

# ==========================================
# 1. LES INN CSV-DATA
# ==========================================
filnavn = "time_series_60min_singleindex.csv"  # Bytt ut med navnet på filen din

# Les inn CSV (Open Power System Data har normalt komma som separator)
try:
    df = pd.read_csv(filnavn)
except:
    df = pd.read_csv(filnavn, sep=";")

# Finn en kolonne med lastdata (f.eks. norsk eller tysk forbruk: 'NO_load_actual_entsoe_transparency')
# Vi henter ut de første 24 timene (et enkelt døgn)
load_col = [c for c in df.columns if "load" in c.lower() or "forbruk" in c.lower()]
if load_col:
    forbruk_data = df[load_col[0]].dropna().iloc[0:24].values
else:
    # Hvis kolonnenavn ikke matcher, tar vi kolonne 1
    forbruk_data = df.iloc[0:24, 1].values

t_data = np.arange(0, 24)  # Timer 0 til 23


# ==========================================
# 2. DEFINÉR MODELLEN (3 KOMPONENTER)
# ==========================================
# Komponent 1: Nattperiode (mu1 ~ kl. 03)
# Komponent 2: Morgentopp (mu2 ~ kl. 08)
# Komponent 3: Kveldstopp (mu3 ~ kl. 18)
def modell_3komp(t, L0, A1, mu1, sigma1, A2, mu2, sigma2, A3, mu3, sigma3):
    g1 = A1 * np.exp(-((t - mu1) ** 2) / (2 * sigma1**2))
    g2 = A2 * np.exp(-((t - mu2) ** 2) / (2 * sigma2**2))
    g3 = A3 * np.exp(-((t - mu3) ** 2) / (2 * sigma3**2))
    return L0 + g1 + g2 + g3


# Startgjett for curve_fit: [L0, A1, mu1, sigma1, A2, mu2, sigma2, A3, mu3, sigma3]
min_val = np.min(forbruk_data)
max_val = np.max(forbruk_data)
amp_gjett = (max_val - min_val) / 2

p0 = [
    min_val,  # L0
    amp_gjett / 2,
    3,
    2.0,  # Nattperiode (kl. 03)
    amp_gjett,
    8,
    2.0,  # Morgentopp (kl. 08)
    amp_gjett,
    18,
    2.5,  # Kveldstopp (kl. 18)
]

# Tilpass parametrene automatisk til CSV-dataene
popt, _ = curve_fit(modell_3komp, t_data, forbruk_data, p0=p0)

# Hent ut optimale parametere
L0_opt, A1_opt, mu1_opt, sig1_opt, A2_opt, mu2_opt, sig2_opt, A3_opt, mu3_opt, sig3_opt = (
    popt
)

# Tett tidsvektor for jevne kurver i plottene
t_smooth = np.linspace(0, 23, 200)
l_modell_smooth = modell_3komp(t_smooth, *popt)

# ==========================================
# 3. UTSKRIFT AV LIGNING OG PARAMETERE
# ==========================================
print("=== PARAMETERVERDIER ===")
print(f"L0 (Grunnlast) : {L0_opt:.2f}")
print(f"Komponent 1 (Natt)  : A1 = {A1_opt:.2f}, mu1 = {mu1_opt:.2f}, sigma1 = {sig1_opt:.2f}")
print(f"Komponent 2 (Morgen): A2 = {A2_opt:.2f}, mu2 = {mu2_opt:.2f}, sigma2 = {sig2_opt:.2f}")
print(f"Komponent 3 (Kveld) : A3 = {A3_opt:.2f}, mu3 = {mu3_opt:.2f}, sigma3 = {sig3_opt:.2f}\n")

print("=== ENDELIG LIGNING ===")
ligning_str = (
    f"L(t) = {L0_opt:.2f} + "
    f"{A1_opt:.2f}*exp(-((t - {mu1_opt:.2f})^2)/(2*{sig1_opt:.2f}^2)) + "
    f"{A2_opt:.2f}*exp(-((t - {mu2_opt:.2f})^2)/(2*{sig2_opt:.2f}^2)) + "
    f"{A3_opt:.2f}*exp(-((t - {mu3_opt:.2f})^2)/(2*{sig3_opt:.2f}^2))"
)
print(ligning_str)

# ==========================================
# 4. PLOTTING (LEVERANSE)
# ==========================================
fig, axs = plt.subplots(3, 1, figsize=(9, 11))

# Plott 1: Observerte data
axs[0].plot(
    t_data,
    forbruk_data,
    "ro-",
    label="Observerte data (CSV)",
    linewidth=2,
    markersize=5,
)
axs[0].set_title("1. Observerte data fra CSV")
axs[0].set_xlabel("Tid t (timer)")
axs[0].set_ylabel("Belastning")
axs[0].grid(True)
axs[0].legend()

# Plott 2: Modellert kurve
axs[1].plot(
    t_smooth,
    l_modell_smooth,
    "b-",
    label="Modellert kurve L(t)",
    linewidth=2,
)
axs[1].set_title("2. Modellert kurve (3 komponenter)")
axs[1].set_xlabel("Tid t (timer)")
axs[1].set_ylabel("Belastning")
axs[1].grid(True)
axs[1].legend()

# Plott 3: Begge vist samtidig
axs[2].plot(
    t_data,
    forbruk_data,
    "ro",
    label="Observerte data (CSV)",
    markersize=6,
)
axs[2].plot(
    t_smooth,
    l_modell_smooth,
    "b-",
    label="Modellert kurve L(t)",
    linewidth=2,
)
axs[2].set_title("3. Sammenligning: Observerte data vs. Modellert kurve")
axs[2].set_xlabel("Tid t (timer)")
axs[2].set_ylabel("Belastning")
axs[2].grid(True)
axs[2].legend()

plt.tight_layout()
plt.show()