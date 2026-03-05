# Visualizaciones del Propagador Fractal TEU 🌌

Este repositorio contiene scripts de simulación auxiliares y visualizaciones matemáticas para el modelo **Topological Electron Universe (TEU)**. 

Mientras que los cálculos analíticos duros de la QED se alojan en el repositorio principal TEU, este espacio está dedicado a explorar la naturaleza estocástica y geométrica del vacío cuántico, centrándose específicamente en cómo las topologías fractales generan la masa inercial a través de sub-difusión anómala.

![Nube Cuántica TEU](poner_aqui_la_ruta_de_tu_imagen.png)

## La Física: Simulando el *Mass Gap* (Génesis de la Masa)

El script `fractal_propagator_sim.py` demuestra visualmente la emergencia de la masa del electrón sin depender de campos escalares externos (como el mecanismo de Higgs). Lo logra simulando la **Integral de Caminos de Feynman Fractal**.

### 1. El Propagador Fractal de Golmankhaneh ($K_F^\alpha$)
En la Mecánica Cuántica estándar, las partículas exploran todos los caminos posibles en un espacio euclídeo suave. Sin embargo, basándonos en la formulación del $F^\alpha$-Cálculo para curvas no diferenciables (Golmankhaneh & Baleanu, 2013), la amplitud de probabilidad (el Propagador $K_F^\alpha$) de que una partícula se mueva a través de un vacío tipo Cantor viene dada por:

$$K_{F}^{\alpha} = \int \mathcal{D}_{F}^{\alpha} \mathbf{w} \, \exp\left(\frac{i}{\hbar} \mathcal{S}_{fractal}\right)$$

Aquí, la integración se realiza sobre la medida fractal $\mathcal{D}_F^\alpha$, y $\mathcal{S}_{fractal}$ es la acción cuántica modificada.

### 2. La Rigidez Geométrica TEU ($K_{geo}$)
¿Cómo se conecta el modelo TEU con este propagador? En nuestro marco teórico, el Laplaciano euclídeo se proyecta sobre la variedad fractal, generando una impedancia espacial intrínseca conocida como **Rigidez Geométrica ($K_{geo}$)**. 

Derivada analíticamente del momento magnético anómalo de la QED ($g-2$), el vacío TEU posee una rigidez exacta de:
$$K_{geo} \approx 2.659$$

### 3. El Puente: El Exponente de Hurst ($H$)
Para simular esta acción analítica ($\mathcal{S}_{fractal}$) usando métodos estocásticos de Monte Carlo, traducimos la rigidez geométrica a una dimensión de caminata aleatoria ($d_w$). El **Exponente de Hurst ($H$)** correspondiente es simplemente la inversa de esta rigidez:

$$H = \frac{1}{K_{geo}} \approx 0.375$$

### ¿Cómo funciona el código? (Síntesis Espectral)
El script en Python no resuelve la integral infinita de Feynman por fuerza bruta. En su lugar, simula el resultado fenomenológico utilizando **Ruido Gaussiano Fraccionario (fGn)** mediante Síntesis Espectral:

1. Un vacío de Minkowski estándar no tiene fricción topológica ($K_{geo}=2 \implies H=0.5$), lo que resulta en ruido blanco normal. La partícula se difunde libremente.
2. Al inyectar el parámetro TEU ($H = 0.375$) en el espectro de potencia de Fourier ($S(f) \propto f^{-(1-2H)}$), el algoritmo obliga a las frecuencias a generar pasos correlacionados negativamente (Régimen Anti-persistente).
3. **El Resultado:** El paquete de ondas cuántico simulado ($|\Psi|^2$) no puede expandirse libremente. Se repliega continuamente sobre sí mismo debido a los huecos topológicos (polvo de Cantor), creando un núcleo de probabilidad denso y localizado.

**Este confinamiento geométrico es el fenómeno macroscópico que nosotros medimos empíricamente como Masa Inercial.**


![Nube Cuántica](img/figura3_nube_cuantica_high_res 2.png)

# figura3_nube_cuantica_high_res 2.pngVisualización 2: Nube Cuántica y el Origen de la Masa ($|\Psi|^2$)

Este apartado del repositorio presenta la simulación de densidad `simulacion_nube_cuantica.py`. Esta simulación visualiza la consecuencia macroscópica directa de las trayectorias fractales generadas por el modelo TEU.

![Densidad de Probabilidad Cuántica](img/figura3_nube_cuantica_high_res.png)

## Las Matemáticas de la Masa: Confinamiento por Sub-difusión

Mientras que la mecánica cuántica canónica y la Ecuación de Schrödinger asumen un espaciotiempo liso, el universo TEU postula que el espacio subatómico está gobernado por una red métrica de Cantor. Esto tiene una consecuencia cinemática ineludible: la **Difusión Anómala**.



### 1. El Vínculo Topología-Cinemática
Como se demostró en el modelo TEU, la interacción analítica del Electromagnetismo genera una "fricción" en el operador Laplaciano denominada **Rigidez Geométrica ($K_{geo}$)**. En la teoría del transporte estocástico, la dificultad para atravesar esta geometría define la dimensión de la caminata, la cual fija el **Exponente de Hurst ($H$)**:

$$H = \frac{1}{K_{geo}} = \frac{1}{2.659} \approx 0.376$$

### 2. Ecuación de Varianza de la Posición
En un vacío estándar de Minkowski (donde $H = 0.5$), un paquete de ondas sin masa se difunde libremente, y su Desplazamiento Cuadrático Medio (MSD) crece linealmente con el tiempo ($\langle x^2 \rangle \propto t$).

Sin embargo, dado que el modelo TEU arroja $H < 0.5$, el electrón entra en un régimen de **Sub-difusión Fuerte** o comportamiento *anti-persistente*. La ecuación que gobierna la propagación de este paquete es:

$$\langle x^2(t) \rangle \propto t^{2H} \approx t^{0.75}$$

### ¿Qué hace el script en Python?
El script genera $5000$ caminos estocásticos de memoria larga y calcula su campo de densidad probabilística global ($|\Psi|^2$) a través de un histograma suavizado 2D. 

**Interpretación Física:** Al crecer la varianza con un exponente menor a 1 ($\approx 0.75$), las partículas colisionan estadísticamente contra la "Escalera del Diablo" métrica y son empujadas hacia atrás, rellenando el espacio localmente. Esta trampa topológica crea un núcleo negro ultra-denso en el centro de la simulación. La resistencia intrínseca a propagarse libremente inducida por esta sub-difusión es precisamente lo que nosotros medimos fenotípicamente como **Masa Inercial**.


## Uso
Simplemente ejecuta el script de Python para generar los gráficos en alta resolución (PDF/PNG) de la nube cuántica:
```bash
python fractal_propagator_sim.py
