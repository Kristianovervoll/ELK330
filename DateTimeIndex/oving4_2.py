import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(
    'load_data.csv',
    index_col="Time(Local)",
    parse_dates=True,
    dayfirst=True)

print(f'First 5 rows:\n {df.head()}')

print(f'Tidspunkt:\n {df.index[0]}')

obs = df.loc[pd.to_datetime("01.01.2026 03:00:00 +01:00", dayfirst=True)]
print(obs)


lastprofil = df.loc[pd.to_datetime("02.05.2026 00:00:00 +01:00", dayfirst=True):pd.to_datetime("02.05.2026 23:00:00 +01:00", dayfirst=True)]

lastprofil["Consumption"] = (
    lastprofil["Consumption"]
    .str.replace(",", ".")
    .astype(float)
)

lastprofil["Consumption"].plot(
    marker="o",
    title="Lastprofil 2. mai 2026",
    xlabel="Tid",
    ylabel="Forbruk",
    linestyle=":",
    color="magenta"
)

plt.xticks(rotation=45)
plt.tight_layout()
plt.grid()
plt.show()

