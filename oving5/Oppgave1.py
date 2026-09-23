import matplotlib.pyplot as plt
import numpy as np


# 1. Definér modellfunksjonen
def modell_L(t, L0, A, mu, sigma):
    t = np.asarray(t, dtype=float)
    A = np.atleast_1d(A)
    mu = np.atleast_1d(mu)
    sigma = np.atleast_1d(sigma)

    L = np.full_like(t, L0, dtype=float)
    for A_i, mu_i, sigma_i in zip(A, mu, sigma):
        L += A_i * np.exp(-((t - mu_i) ** 2) / (2 * sigma_i**2))
    return L


# 2. Sett opp tidsakse (0 til 24 timer) og grunnlast L0
t = np.linspace(0, 24, 500)
L0 = 10.0

# -------------------------------------------------------------
# EKSPERIMENT 1: Endre tidspunkt for toppen (mu)
# -------------------------------------------------------------
plt.figure(figsize=(8, 4))
plt.plot(
    t,
    modell_L(t, L0, A=15, mu=8, sigma=1.5),
    label="Tidlig topp (mu = 8 kl. 08)",
)
plt.plot(
    t,
    modell_L(t, L0, A=15, mu=14, sigma=1.5),
    "--",
    label="Senere topp (mu = 14 kl. 14)",
)
plt.title("Eksperiment 1: Effekten av å endre mu (tidspunkt for topp)")
plt.xlabel("Tid t (timer)")
plt.ylabel("Belastning L(t)")
plt.grid(True)
plt.legend()
plt.show()

# -------------------------------------------------------------
# EKSPERIMENT 2: Endre amplitude/høyde (A)
# -------------------------------------------------------------
plt.figure(figsize=(8, 4))
plt.plot(t, modell_L(t, L0, A=10, mu=12, sigma=1.5), label="Lav topp (A = 10)")
plt.plot(
    t,
    modell_L(t, L0, A=25, mu=12, sigma=1.5),
    "--",
    label="Høy topp (A = 25)",
)
plt.title("Eksperiment 2: Effekten av å endre A (amplituden / høyden)")
plt.xlabel("Tid t (timer)")
plt.ylabel("Belastning L(t)")
plt.grid(True)
plt.legend()
plt.show()

# -------------------------------------------------------------
# EKSPERIMENT 3: Endre bredden på toppen (sigma)
# -------------------------------------------------------------
plt.figure(figsize=(8, 4))
plt.plot(
    t,
    modell_L(t, L0, A=15, mu=12, sigma=0.8),
    label="Smal/spiss topp (sigma = 0.8)",
)
plt.plot(
    t,
    modell_L(t, L0, A=15, mu=12, sigma=3.0),
    "--",
    label="Bred/utflatet topp (sigma = 3.0)",
)
plt.title("Eksperiment 3: Effekten av å endre sigma (bredden)")
plt.xlabel("Tid t (timer)")
plt.ylabel("Belastning L(t)")
plt.grid(True)
plt.legend()
plt.show()