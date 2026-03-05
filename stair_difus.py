import numpy as np
import matplotlib.pyplot as plt
from scipy.special import gamma
import warnings

warnings.filterwarnings("ignore")

def generate_scientific_plots():
    print("Generating vectorized scientific plots...")

    # =========================================================================
    # 1. PAPER STYLE CONFIGURATION
    # =========================================================================
    plt.style.use('default')

    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["DejaVu Serif", "Times New Roman"],
        "mathtext.fontset": "cm",
        "font.size": 12,
        "axes.linewidth": 0.8,
        "axes.labelsize": 12,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 10,
        "lines.linewidth": 1.2,
        "grid.linestyle": ":",
        "grid.color": "gray",
        "grid.alpha": 0.5,
        "xtick.direction": "in",
        "ytick.direction": "in",
        "savefig.format": "pdf",
        "pdf.fonttype": 42
    })

    # =========================================================================
    # 2. FIGURE 1: THE FRACTAL STAIRCASE (S_F Function)
    # =========================================================================
    print("Plotting Figure 1: Fractal Staircase...")
    mu = 0.7575
    A = 0.5974
    k = 1.4819

    x = np.logspace(-1, 1.5, 2000)
    trend = (x**mu) / gamma(mu + 1)
    oscillation = 1 + A * np.sin(k * np.log(x))
    y_fractal = trend * oscillation
    y_euclid = x

    fig1, ax1 = plt.subplots(figsize=(7, 5))

    ax1.plot(x, y_euclid, 'k--', linewidth=1, label=r'Euclidean Metric ($\mu=1$)')
    ax1.plot(x, y_fractal, 'k-', linewidth=1.2, label=r'Fractal Vacuum $S_F^\mu(x)$')

    # Lacunarity zone (Hatching for B/W paper style)
    ax1.fill_between(x, y_euclid, y_fractal, where=(y_euclid > y_fractal),
                     facecolor='none', hatch='////', edgecolor='gray', linewidth=0.0,
                     label='Lacunarity (Missing Mass)')

    ax1.set_xlabel(r'Metric Distance $x$ [Arbitrary Units]')
    ax1.set_ylabel(r'Effective Mass $S_F^\mu(x)$')
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_xlim(x[0], x[-1])
    ax1.legend(loc='upper left', frameon=False)

    textstr = '\n'.join((
        r'$\mu = 0.7575$',
        r'$A = 0.5974$',
        r'$k = 1.4819$'
    ))
    props = dict(boxstyle='square,pad=0.5', facecolor='white', alpha=1.0, edgecolor='black')
    ax1.text(0.95, 0.05, textstr, transform=ax1.transAxes,
             verticalalignment='bottom', horizontalalignment='right', bbox=props)

    fig1.tight_layout()

    # Save FIGURE 1 (PDF and PNG)
    f1_pdf = "figura1_staircase.pdf"
    f1_png = "figura1_staircase.png"
    fig1.savefig(f1_pdf, bbox_inches='tight')
    fig1.savefig(f1_png, dpi=300, bbox_inches='tight')
    print(f"  -> Saved {f1_pdf} and {f1_png}")
    plt.close(fig1)

    # =========================================================================
    # 3. FIGURE 2: ANOMALOUS DIFFUSION PATH
    # =========================================================================
    print("Plotting Figure 2: Anomalous Diffusion Path...")
    K_geo = 2.6605
    H = 1.0 / K_geo  # Hurst ~ 0.375
    n_steps = 20000

    np.random.seed(137) # Poetic fine-structure constant seed

    def fbm_spectral_path(n, H):
        f = np.fft.rfftfreq(n)
        f[0] = 1e-9
        
        exponent = H + 0.5
        amplitude = 1.0 / (f**exponent)
        amplitude[0] = 0
        
        phase = np.random.uniform(0, 2*np.pi, len(f))
        complex_signal = amplitude * np.exp(1j * phase)
        path = np.fft.irfft(complex_signal)
        return path

    x_path = fbm_spectral_path(n_steps, H)
    y_path = fbm_spectral_path(n_steps, H)

    x_path -= x_path[0]
    y_path -= y_path[0]

    fig2, ax2 = plt.subplots(figsize=(6, 6))

    ax2.plot(x_path, y_path, 'k-', linewidth=0.3, alpha=0.9)
    ax2.plot(x_path[0], y_path[0], 'o', color='black', markersize=5, fillstyle='none', label=r'Start ($t_0$)')
    ax2.plot(x_path[-1], y_path[-1], 's', color='black', markersize=5, fillstyle='full', label=r'End ($t_{final}$)')

    ax2.set_xlabel(r'Spatial Coordinate $q_1$')
    ax2.set_ylabel(r'Spatial Coordinate $q_2$')
    ax2.set_xticks([])
    ax2.set_yticks([])
    ax2.set_aspect('equal')
    ax2.legend(loc='upper right', frameon=True, edgecolor='black', fontsize=9)

    annot = '\n'.join((
        r'Vacuum Topology:',
        r'Walk Dim $d_w \approx 2.66$',
        r'Hurst $H \approx 0.375$',
        r'Regime: Anti-persistent'
    ))
    
    ax2.text(0.03, 0.03, annot, transform=ax2.transAxes, fontsize=10,
             verticalalignment='bottom', bbox=props)

    fig2.tight_layout()

    # Save FIGURE 2 (PDF and PNG)
    f2_pdf = "figura2_diffusion.pdf"
    f2_png = "figura2_diffusion.png"
    fig2.savefig(f2_pdf, bbox_inches='tight')
    fig2.savefig(f2_png, dpi=300, bbox_inches='tight')
    print(f"  -> Saved {f2_pdf} and {f2_png}")
    plt.close(fig2)

    print("\nProcess completed successfully!")

    # Attempt automatic download for Google Colab
    try:
        from google.colab import files
        for f in [f1_pdf, f1_png, f2_pdf, f2_png]:
            files.download(f)
    except ImportError:
        pass

if __name__ == "__main__":
    generate_scientific_plots()
