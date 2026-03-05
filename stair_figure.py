import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import warnings

# Silenciar avisos menores
warnings.filterwarnings("ignore")

def teu_barcode_plot():
    print("=======================================================================")
    print("      TEU ELECTRON TOPOLOGY: BARCODE VISUALIZATION")
    print("=======================================================================")

    # 1. PARÁMETROS TEU
    mu = 0.757603              # Dimensión Fractal

    # Cálculo del Gap Ratio (Tamaño relativo del agujero)
    # Derivado de la dimensión fractal: 2 * ((1-gap)/2)^mu = 1
    gap_ratio = 1 - 2**(1 - 1/mu)

    # 2. GENERADOR DE GAPS (Para dibujar las franjas blancas)
    vacuum_gaps = []

    def compute_gaps(x0, x1, depth, max_visual_depth):
        if depth == 0:
            return

        length = x1 - x0
        gap_size = length * gap_ratio
        segment_size = (length - gap_size) / 2

        # Coordenadas del Gap Central
        gap_start = x0 + segment_size
        gap_end = x1 - segment_size

        # Guardamos el gap si es visible
        if depth <= max_visual_depth:
            vacuum_gaps.append((gap_start, gap_end))

        # Recursión en los segmentos laterales (Masa)
        compute_gaps(x0, gap_start, depth-1, max_visual_depth)
        compute_gaps(gap_end, x1, depth-1, max_visual_depth)

    # 3. GENERADOR DE LA CURVA (Masa Acumulada)
    def recursive_points(x0, x1, y0, y1, d):
        if d == 0: 
            return [x0, x1], [y0, y1]
        
        L = x1 - x0
        gap = L * gap_ratio
        seg = (L - gap) / 2
        ym = (y0 + y1) / 2
        
        lx, ly = recursive_points(x0, x0 + seg, y0, ym, d - 1)
        rx, ry = recursive_points(x1 - seg, x1, ym, y1, d - 1)
        
        # Al unir las listas, se crea automáticamente la línea plana sobre el gap
        return lx + rx, ly + ry

    # Ejecutamos cálculos
    # A. Gaps (Profundidad 5 es ideal para la vista)
    compute_gaps(0, 1, depth=6, max_visual_depth=5)

    # B. Curva (Profundidad 8 para que la línea negra sea perfecta)
    xp, yp = recursive_points(0, 1, 0, 9.109, d=8)

    # 4. GRAFICADO ESTILO "CÓDIGO DE BARRAS"
    # Solución al error de fuentes: Cadena de fuentes de respaldo
    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["DejaVu Serif", "Times New Roman", "serif"],
        "font.size": 12,
        "figure.figsize": (9, 6)
    })

    fig, ax = plt.subplots()

    # FONDO: Gris Claro (Representa la MASA POTENCIAL)
    ax.set_facecolor('#E0E0E0') 

    # FRANJAS: Blancas (Representan el VACÍO/GAP)
    for (start, end) in vacuum_gaps:
        ax.axvspan(start, end, facecolor='white', alpha=1.0, edgecolor=None)

    # LÍNEA: La Escalera del Diablo (Negra Sólida)
    ax.plot(xp, yp, 'k-', linewidth=1.5, label=rf'Mass Accumulation ($\mu \approx {mu:.3f}$)')

    # REFERENCIA: Línea Euclídea (Punteada)
    ax.plot([0, 1], [0, 9.109], 'k--', linewidth=0.8, alpha=0.5, label='Euclidean Space')

    # Decoración
    ax.set_title(r"Internal Topology of the Electron: Mass vs. Vacuum", fontsize=14, pad=15)
    ax.set_xlabel(r"Normalized Scale ($\lambda$)", fontsize=12)
    ax.set_ylabel(r"Integrated Mass ($10^{-31}$ kg)", fontsize=12)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 9.5)

    # Leyenda personalizada
    custom_lines = [
        Line2D([0], [0], color='k', lw=1.5),
        patches.Patch(facecolor='#E0E0E0', edgecolor='k'),
        patches.Patch(facecolor='white', edgecolor='k')
    ]

    ax.legend(custom_lines, ['Mass Function (Devil\'s Staircase)', 'Mass Regions (Gray)', 'Vacuum Gaps (White)'],
              loc='upper left', frameon=True, edgecolor='black', fancybox=False)

    plt.tight_layout()

    # GUARDADO MULTIFORMATO
    filename_base = "TEU_Topology_Barcode"
    
    plt.savefig(f"{filename_base}.pdf", bbox_inches='tight')
    plt.savefig(f"{filename_base}.svg", bbox_inches='tight')
    plt.savefig(f"{filename_base}.png", dpi=300, bbox_inches='tight') # <-- PNG para el README
    
    print(f"Gráficas guardadas: {filename_base} (.pdf, .svg, .png)")

    # Descarga automática en Colab
    try:
        from google.colab import files
        files.download(f"{filename_base}.pdf")
        files.download(f"{filename_base}.png")
    except ImportError:
        pass

if __name__ == "__main__":
    from matplotlib.lines import Line2D # Importado aquí para evitar errores arriba
    teu_barcode_plot()
