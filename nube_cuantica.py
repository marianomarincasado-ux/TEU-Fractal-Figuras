import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from scipy.ndimage import gaussian_filter
import warnings

# Silenciar avisos de fuentes
warnings.filterwarnings("ignore")

def simulacion_nube_cuantica_suave():
    print("Generando Nube de Probabilidad Cuántica (Alta Resolución)...")

    # 1. Configuración Estilo Paper
    plt.style.use('default')
    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["DejaVu Serif", "Times New Roman"],
        "mathtext.fontset": "cm",
        "font.size": 12
    })

    # 2. Parámetros Físicos (DEDUCIDOS DE TU TEORÍA)
    K_geo = 2.659455 
    H = 1.0 / K_geo  

    n_paths = 5000   
    n_steps = 1000   

    # 3. Generador de Caminos (Síntesis Espectral)
    def generate_fbm_paths(n_paths, n_steps, H):
        f = np.fft.rfftfreq(n_steps)
        f[0] = 1e-9 
        beta = 1 - 2*H
        amplitude = np.sqrt(1.0 / (f**beta))
        amplitude[0] = 0
        phases = np.random.uniform(0, 2*np.pi, size=(n_paths, len(f)))
        complex_signal = amplitude * np.exp(1j * phases)
        noise = np.fft.irfft(complex_signal, n=n_steps, axis=1)
        paths = np.cumsum(noise, axis=1)
        paths = paths - paths[:, 0:1]
        return paths

    x_paths = generate_fbm_paths(n_paths, n_steps, H)
    y_paths = generate_fbm_paths(n_paths, n_steps, H)

    all_x = x_paths.flatten()
    all_y = y_paths.flatten()

    # 4. GRÁFICO: NUBE DE PROBABILIDAD
    fig, ax = plt.subplots(figsize=(7, 7))

    for i in range(100):
        ax.plot(x_paths[i], y_paths[i], color='black', alpha=0.02, linewidth=0.1)

    limit = np.percentile(np.abs(all_x), 98) 
    bins = 200 

    density, x_edges, y_edges = np.histogram2d(
        all_x, all_y, 
        bins=bins, 
        range=[[-limit, limit], [-limit, limit]]
    )

    density_smooth = gaussian_filter(density.T, sigma=1.5)

    cmap = LinearSegmentedColormap.from_list('quantum_cloud', 
                                             ['white', '#d9d9d9', '#888888', '#333333', 'black'], N=256)

    im = ax.imshow(density_smooth, origin='lower', 
                   extent=[-limit, limit, -limit, limit],
                   cmap=cmap, interpolation='bicubic', aspect='equal')

    # ==========================================
    # 5. ESTÉTICA Y ECUACIONES (CORREGIDO)
    # ==========================================
    ax.set_xticks([])
    ax.set_yticks([])

    ax.set_title(r'Fractal Propagator Density $|\Psi|^2$', fontsize=15, pad=15)
    ax.set_xlabel(r'Quantum Position $\hat{q}_1$', fontsize=13)
    ax.set_ylabel(r'Quantum Position $\hat{q}_2$', fontsize=13)

    # Texto unificado, usando MAYÚSCULAS en lugar de superposiciones problemáticas
    legend_text = (
        "TEU GEOMETRY:\n"
        r"$K_{geo} \approx 2.66 \rightarrow H \approx 0.376$" "\n"
        "---------------------------\n"
        "SUB-DIFFUSION CREATES MASS:\n"
        r"$\langle x^2 \rangle \propto t^{2H} \ll t^1$"
    )

    props = dict(boxstyle='square,pad=0.5', facecolor='white', alpha=0.9, edgecolor='black', linewidth=0.8)
    
    # Se imprime una única vez, sin capas extra
    ax.text(0.04, 0.04, legend_text, transform=ax.transAxes, fontsize=11,
            verticalalignment='bottom', bbox=props, family='serif')

    for spine in ax.spines.values():
        spine.set_linewidth(1.2)

    plt.tight_layout()

    # ==========================================
    # 6. GUARDAR Y DESCARGAR FORMATOS
    # ==========================================
    filename_pdf = "figura3_nube_cuantica_high_res.pdf"
    filename_png = "figura3_nube_cuantica_high_res.png"

    plt.savefig(filename_pdf, bbox_inches='tight')
    print(f"Generado: {filename_pdf}")

    plt.savefig(filename_png, dpi=300, bbox_inches='tight')
    print(f"Generado: {filename_png}")

    plt.close()

    try:
        from google.colab import files
        files.download(filename_pdf)
        files.download(filename_png)
    except ImportError:
        pass

if __name__ == "__main__":
    simulacion_nube_cuantica_suave()
