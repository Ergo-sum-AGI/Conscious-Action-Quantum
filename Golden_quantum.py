# golden_quantum.py
# Generates:
# 1. α⁻¹ from Golden Function
# 2. Rydberg constant fit (zero modulation)
# 3. He hyperfine overtone prediction
# 4. Saves plot: rydberg_fit.png

import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import Rydberg, alpha

# Golden ratio
phi = (1 + np.sqrt(5)) / 2

# Golden Function (Pellis 2025)
alpha_inv_gf = 360 * phi**(-2) - 2 * phi**(-3) + (3 * phi)**(-5)
print(f"Golden Function α⁻¹: {alpha_inv_gf:.9f}")

# CODATA 2018
alpha_inv_codata = 1 / alpha
print(f"CODATA 2018 α⁻¹:     {alpha_inv_codata:.9f}")
print(f"Error: {(alpha_inv_gf - alpha_inv_codata)/alpha_inv_codata * 100:.3e}%")

# Rydberg fit: R_infinity should match exactly (amp=0)
R_pred = Rydberg * (alpha_inv_gf / alpha_inv_codata)
print(f"Predicted R∞: {R_pred:.10f} m⁻¹")
print(f"Actual R∞:     {Rydberg:.10f} m⁻¹")
print(f"R error: {(R_pred - Rydberg)/Rydberg * 100:.3e}%")

# He hyperfine overtone: ϕ⁻² × 1420 MHz
f_1420 = 1420.405751768  # MHz (hydrogen 21cm)
f_he = f_1420 * (1/phi**2)
print(f"He overtone: {f_he:.3f} MHz")

# Plot: Rydberg "fit" (perfect match)
freq = np.linspace(0, 1e6, 100)
rydberg_line = np.full_like(freq, Rydberg)
rydberg_pred = np.full_like(freq, R_pred)

plt.figure(figsize=(8,5))
plt.plot(freq, rydberg_line, 'k-', label='CODATA R∞', linewidth=2)
plt.plot(freq, rydberg_pred, 'r--', label='Golden Function R∞', linewidth=2)
plt.fill_between(freq, rydberg_line, rydberg_pred, color='red', alpha=0.2)
plt.title('Rydberg Constant: Golden Function vs CODATA')
plt.xlabel('Dummy Frequency (Hz)')
plt.ylabel('R∞ (m⁻¹)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('rydberg_fit.png', dpi=300)
plt.close()

print("Plot saved: rydberg_fit.png")