import pandas as pd

df = pd.read_csv('load_data.csv', index_col="Time(Local)", parse_dates=True, dayfirst=True)

consumption = df["Consumption"].str.replace(",", ".").astype(float)
production = df["Production"].str.replace(",", ".").astype(float)

df["Netto"] = (
    production - consumption
)

print(f'Max production: \n\t {max(production)}\n'
      f'Min production: \n\t {min(production)}\n'
      f'Average production: \n\t {sum(production)/len(production)}\n')

print(f'Max Netto: \n\t {max(df["Netto"])}\n'
      f'Min Netto: \n\t {min(df["Netto"])}\n')

max_netto_tid = df['Netto'].idxmax()
min_netto_tid = df['Netto'].idxmin()

print(f'Maksimal nettoeffekt: {df.loc[max_netto_tid, "Netto"]:.2f} '
      f'klokken {max_netto_tid}')
print(f'Minimal nettoeffekt: {df.loc[min_netto_tid, "Netto"]:.2f} '
      f'klokken {min_netto_tid}')

print(production.sum())