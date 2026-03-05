import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import scipy.special as sp
import warnings

warnings.filterwarnings("ignore")

def generate_teu_hyperspace_dashboard():
    print("===================================================================")
    print(" GENERATING TEU HYPERSPACE DASHBOARD (OpenFermion Style)           ")
    print("===================================================================")

    # 1. PARÁMETROS TEU
    MU_FRACTAL = 0.757603135
    LACUNARITY_A = 0.596980759
    K_MOIRE = 1.481998886
    PHI_MOIRE = -0.282072371
    Z_MU = 1.0 / sp.gamma(MU_FRACTAL + 1.0)
    
    # 2. FUNCIÓN DEL INTEGRANDO (Fractal Dirac Action)
    def fractal_dirac_action(r):
        r = np.clip(r, 1e-10, None)
        jacobian_transform = (r**(MU_FRACTAL - 1.0)) * Z_MU
        moire_phase = np.abs(np.sin(K_MOIRE * np.log(r) + PHI_MOIRE))
        connection_variance = LACUNARITY_A * (jacobian_transform**2) * moire_phase
        return connection_variance * np.exp(-1.0 * MU_FRACTAL * r)

    # 3. CONFIGURACIÓN DEL DASHBOARD (Tema Oscuro)
    plt.style.use('dark_background')
    # Fuente segura
    plt.rcParams.update({'font.family': 'sans-serif', 'font.sans-serif': ['Arial', 'DejaVu Sans']})
    
    fig = plt.figure(figsize=(14, 8))
    fig.suptitle('TEU AB INITIO MASS EMERGENCE: 4D VEGAS INTEGRATION KERNEL', 
                 fontsize=18, fontweight='bold', color='white', y=0.96)

    # --- PANEL 1: CORTE TRANSVERSAL DEL HIPERESPACIO 4D ---
    ax1 = plt.subplot(1, 2, 1)
    
    x = np.linspace(-1.0, 1.0, 400)
    y = np.linspace(-1.0, 1.0, 400)
    X, Y = np.meshgrid(x, y)
    
    # Norma euclídea 4D truncada (corte transversal en z=0.05, w=0.05)
    R_4D_slice = np.sqrt(X**2 + Y**2 + 0.05**2 + 0.05**2)
    Z_vals = fractal_dirac_action(R_4D_slice)

    contour = ax1.contourf(X, Y, Z_vals, levels=50, cmap='magma', norm=LogNorm(vmin=1e-3, vmax=np.max(Z_vals)))
    cbar = plt.colorbar(contour, ax=ax1, fraction=0.046, pad=0.04)
    cbar.set_label('Topological Density (Log Scale)', color='white')
    
    ax1.set_title('Cross-Section of 4D Fractal Dirac Action', fontsize=12, pad=10)
    ax1.set_xlabel('Spatial Coordinate $x_1$')
    ax1.set_ylabel('Spatial Coordinate $x_2$')
    ax1.set_aspect('equal')
    ax1.grid(color='#444444', linestyle='--', alpha=0.5)

    # --- PANEL 2: PERFIL RADIAL (LA RESONANCIA DE MOIRÉ) ---
    ax2 = plt.subplot(2, 2, 2)
    
    r_1d = np.logspace(-4, 0, 1000)
    density_1d = fractal_dirac_action(r_1d)
    
    ax2.plot(r_1d, density_1d, color='#00ffcc', linewidth=2)
    ax2.fill_between(r_1d, 1e-5, density_1d, color='#00ffcc', alpha=0.2)
    
    ax2.set_xscale('log')
    ax2.set_yscale('log')
    ax2.set_title('Radial Integrity: The Moiré Resonance', fontsize=12)
    ax2.set_xlabel('4D Distance $r$ (Log Scale)')
    ax2.set_ylabel('Integrand Amplitude')
    ax2.grid(color='#444444', linestyle=':', alpha=0.5)
    
    # Ecuación (Caja de texto corregida)
    eq_text = r"$\Omega(r) \propto r^{2(\mu-1)} |\sin(k \ln r + \phi)| e^{-\mu r}$"
    props = dict(boxstyle='round,pad=0.5', facecolor='black', alpha=0.8, edgecolor='#00ffcc')
    ax2.text(0.35, 0.8, eq_text, transform=ax2.transAxes, color='white', 
             fontsize=12, bbox=props)

    # --- PANEL 3: CASCADA DE ESCALA DE MASA ---
    ax3 = plt.subplot(2, 2, 4)
    
    m_planck = 2.176e-8
    m_electron = 9.109e-31
    k_geo = 2.659455
    depth = 137.036 / k_geo
    
    labels = ['Planck Mass ($M_P$)', 'Sub-diffusive Attenuation', 'Electron Mass ($m_e$)']
    values = [m_planck, m_planck * np.exp(-depth/2), m_electron]
    y_pos = np.arange(len(labels))
    
    bars = ax3.barh(y_pos, values, color=['#ff0055', '#8844aa', '#00ffcc'], height=0.5)
    
    ax3.set_xscale('log')
    ax3.set_yticks(y_pos)
    ax3.set_yticklabels(labels)
    ax3.invert_yaxis()
    ax3.set_title('Emergent Inertial Mass Cascade', fontsize=12)
    ax3.set_xlabel('Mass (kg) [Log Scale]')
    ax3.grid(axis='x', color='#444444', linestyle='-', alpha=0.3)
    
    ax3.annotate(f'Filter: $\exp(-D) \sim 10^{{-23}}$', xy=(values[1], 1), 
                 xytext=(1e-15, 0.5), color='white',
                 arrowprops=dict(facecolor='white', shrink=0.05, width=1, headwidth=5))

    plt.tight_layout(pad=3.0)
    
    # GUARDAR
    filename_base = "TEU_VEGAS_Dashboard"
    plt.savefig(f"{filename_base}.png", dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.savefig(f"{filename_base}.pdf", bbox_inches='tight', facecolor=fig.get_facecolor())
    print(f"Gráficas guardadas: {filename_base} (.png, .pdf)")
    
    try:
        from google.colab import files
        files.download(f"{filename_base}.png")
    except ImportError:
        pass

if __name__ == "__main__":
    generate_teu_hyperspace_dashboard()
