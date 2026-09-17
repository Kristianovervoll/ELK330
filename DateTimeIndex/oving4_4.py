import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(
    'load_data.csv',
    index_col="Time(Local)",
    parse_dates=True,
    dayfirst=True
)

consumption = df["Consumption"].str.replace(",", ".").astype(float)
production = df["Production"].str.replace(",", ".").astype(float)

df["Netto"] = (
    production - consumption
)

plt.subplot(2, 1, 1)
plt.plot(df.index, consumption, label="Consumption", color="red")
plt.plot(df.index, production, label="Production", color="green")
plt.title("Consumption and Production Over Time")
plt.grid()
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(df.index, df["Netto"], label="Netto", color="blue")
plt.plot(df.index, consumption, label="Consumption", color="red")
plt.plot(df.index, production, label="Production", color="green")

plt.xlabel("Time")
plt.ylabel("Value")
plt.legend()
plt.grid()
plt.show()



