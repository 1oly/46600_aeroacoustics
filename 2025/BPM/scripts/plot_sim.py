import pandas as pd
import matplotlib.pyplot as plt

# Predictions using BPM
results = pd.read_csv("PATH/TO/RESULTS.csv")
# Load measurements:
df = pd.read_excel("PATH/TO/MEASUREMENTS.xlsx",header=0)
freq_values = [250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500, 3150, 4000, 5000]

# filter on AoA and U0
AoA = 2
U0 = 80
filtered_meas = df[(df['AoA_geo'] ==AoA) & (df['U0_enc'] == U0)]
filtered_sim = results[(results['alpha'] ==AoA) & (results['velocity'] == U0)]

plt.figure(figsize=(12, 6))
for index, row in filtered_meas.iterrows():
    plt.semilogx(freq_values, row[[f"{freq}Hz" for freq in freq_values]], label=f"Measurement",linewidth=2)

plt.semilogx(filtered_sim.frequency,filtered_sim.spl_s,linestyle='--',linewidth=2,label=f"BPM ss")
plt.semilogx(filtered_sim.frequency,filtered_sim.spl_p,linestyle='--',linewidth=2,label=f"BPM ps")
plt.xlabel('Frequency [Hz]')
plt.ylabel('dB')
plt.xticks(freq_values,freq_values)
plt.xlim(250,5000)
plt.ylim(50,80)
plt.legend()
plt.grid('both')
plt.tight_layout()
plt.show()

