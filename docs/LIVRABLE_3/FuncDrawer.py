import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter, LogLocator

# Constantes
R = 1590990.258  # en ohms
C = 1e-9         # en farads
L = 40.5e-3      # en henrys
f_min = 1000     # fréquence minimale en Hz
f_max = 490000   # fréquence maximale en Hz

# Plage de fréquences
frequencies = np.logspace(np.log10(f_min), np.log10(f_max), 500)

omega = 2 * np.pi * frequencies  # Pulsations

# Calcul de w0 et Q
w0 = 1 / np.sqrt(L * C)
f0 = 25000  # Fréquence de résonance en Hz
Q = R / np.sqrt(L / C)

# Fonction de transfert |T(w)| et phase phi(w)
T_magnitude = 1 / np.sqrt(1 + Q**2 * ((omega / w0) - (w0 / omega))**2)
T_phase = -np.arctan(Q * ((omega / w0) - (w0 / omega)))

# Gain en dB
gain_db = 20 * np.log10(T_magnitude)
print (gain_db)
# Tracé des diagrammes de Bode
plt.figure(figsize=(12, 8))

# Diagramme de gain
plt.subplot(2, 1, 1)
plt.semilogx(frequencies, gain_db, label='Gain (dB)', color='b')
plt.axvline(f0, color='g', linestyle='--', label=f"Résonance ({f0:.0f} Hz)")  # Ligne verticale à la résonance
plt.title('Diagramme de Bode - Gain et Phase')
plt.ylabel('Gain (dB)')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.legend()
plt.gca().xaxis.set_major_formatter(ScalarFormatter())  # Force normal number format
plt.gca().xaxis.set_minor_locator(LogLocator(base=10.0, subs=np.arange(1.0, 10.0) * 0.1, numticks=10))  # Petits intervalles sur x
plt.gca().grid(True, which='minor', linestyle=':', linewidth=0.5)  # Grille mineure

# Diagramme de phase
plt.subplot(2, 1, 2)
plt.semilogx(frequencies, np.degrees(T_phase), label='Phase (°)', color='r')
plt.axvline(f0, color='g', linestyle='--', label=f"Résonance ({f0:.0f} Hz)")  # Ligne verticale à la résonance
plt.axhline(90, color='blue', linestyle='--', linewidth=0.7, label='+90°')  # Ligne horizontale à +90°
plt.axhline(-90, color='blue', linestyle='--', linewidth=0.7, label='-90°')  # Ligne horizontale à -90°
plt.xlabel('Fréquence (Hz)')
plt.ylabel('Phase (°)')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.legend()
plt.gca().xaxis.set_major_formatter(ScalarFormatter())  # Force normal number format
plt.gca().xaxis.set_minor_locator(LogLocator(base=10.0, subs=np.arange(1.0, 10.0) * 0.1, numticks=10))  # Petits intervalles sur x
plt.gca().grid(True, which='minor', linestyle=':', linewidth=0.5)  # Grille mineure

plt.tight_layout()
plt.show()

