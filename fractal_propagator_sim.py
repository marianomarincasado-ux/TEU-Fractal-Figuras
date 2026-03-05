import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import warnings

# Silenciar avisos de fuentes para ejecución limpia
warnings.filterwarnings("ignore")

def simulate_fractal_feynman_propagator():
    print("Simulating Fractal Feynman Propagator (Golmankhaneh Eq. 16)...")
    print("Applying TEU parameters: H ~ 0.375, K_geo ~ 2.66")

    # 1. CONFIGURACIÓN ESTILO PAPER
    plt.style.use('default')
    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["Times New Roman", "DejaVu Serif"],
        "mathtext.fontset": "cm",
        "font.size": 12
    })

    # 2. PARÁMETROS FÍSICOS TEU
    # Hurst Exponent H = 1 / K_geo.
    # TEU K_geo = 2.659 => H = 0.375
    H = 0.375
    n_paths = 2000    # Número de historias de Feynman (Alta densidad)
    n_steps = 500     # Resolución temporal

    # 3. GENERADOR DE CAMINOS FRACTALES (Fractional Brownian Motion)
    def generate_fbm_paths(n_paths, n_steps, H):
        f = np.fft.rfftfreq(n_steps)
        f[0] = 1e-9 # Evitar división por cero

        # Espectro de potencia para fGn
        beta = 1 - 2*H
        amplitude = np.sqrt(1.0 / (f**beta))
        amplitude[0] = 0

        # Fases aleatorias
        phases = np.random.uniform(0, 2*np.pi, size=(n_paths, len(f)))
        complex_signal = amplitude * np.exp(1j * phases)

        # Ruido y trayectoria
        noise = np.fft.irfft(complex_signal, n=n_steps, axis=1)
        paths = np.cumsum(noise, axis=1)

        # Normalizar al origen
        paths = paths - paths[:, 0:1]
        return paths

    # Generar trayectorias X e Y
    x_paths = generate_fbm_paths(n_paths, n_steps, H)
    y_paths = generate_fbm_paths(n_paths, n_steps, H)

    # 4. CREACIÓN DEL GRÁFICO
    fig, ax = plt.subplots(figsize=(6, 6))

    # Hilos tenues
    for i in range(50): 
        ax.plot(x_paths[i], y_paths[i], color='black', alpha=0.1, linewidth=0.3)

    # Mapa de densidad (Hexbin)
    all_x = x_paths.flatten()
    all_y = y_paths.flatten()
    cmap = LinearSegmentedColormap.from_list('density', ['white', '#cccccc', 'black'])
    hb = ax.hexbin(all_x, all_y, gridsize=50, cmap=cmap, mincnt=1, alpha=0.6, edgecolors='none')

    # 5. ESTÉTICA Y LEYENDAS
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])

    ax.set_title(r'Fractal Propagator $K_{F}^{\alpha}$ (TEU parameters)', fontsize=14, pad=10)
    ax.set_xlabel(r'Fractal Space coordinate $w_1$')
    ax.set_ylabel(r'Fractal Space coordinate $w_2$')

    limit = np.percentile(np.abs(all_x), 98) 
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)

    equation_text = (
        r'$K_{F}^{\alpha} = \int \mathcal{D}_{F}^{\alpha} \mathbf{w} \, \exp\left(\frac{i}{\hbar} \mathcal{S}_{fractal}\right)$' '\n'
        r'-----------------------------------------' '\n'
        r'Simulation Parameters:' '\n'
        r'$\mu \approx 0.7575$ (Fractal Dim.)' '\n'
        r'$H \approx 0.375$ (Anti-persistence)' '\n'
        r'$|\Psi|^2$: Quantum Mass Confinement'
    )

    props = dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='black')
    ax.text(0.05, 0.05, equation_text, transform=ax.transAxes, fontsize=9,
            verticalalignment='bottom', bbox=props)

    plt.tight_layout()

    # ==========================================
    # 6. GUARDAR Y DESCARGAR EN AMBOS FORMATOS
    # ==========================================
    filename_pdf = "figura3_propagador_feynman_english.pdf"
    filename_png = "figura3_propagador_feynman_english.png"

    # Guardar PDF (Calidad Vectorial para el Paper)
    plt.savefig(filename_pdf, bbox_inches='tight')
    print(f"Generated: {filename_pdf}")

    # Guardar PNG (Alta resolución 300 dpi para GitHub README)
    plt.savefig(filename_png, dpi=300, bbox_inches='tight')
    print(f"Generated: {filename_png}")

    plt.close()

    # Si estás en Google Colab, descarga los dos automáticamente
    try:
        from google.colab import files
        files.download(filename_pdf)
        files.download(filename_png)
    except ImportError:
        pass # Si se corre en local, los archivos ya estarán en la carpeta

if __name__ == "__main__":
    simulate_fractal_feynman_propagator()
