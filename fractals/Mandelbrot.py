import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider,RadioButtons, RangeSlider

matplotlib.use('TkAgg')

def mandelbrot_set(x_min: float, x_max: float, y_min: float, y_max: float, n: int, k: int):
    """
    Vypočítá Mandelbrotovu množinu v daném rozsahu.

    Args:
        x_min (float): Minimum reálné části.
        x_max (float): Maximum reálné části.
        y_min (float): Minimum imaginární části.
        y_max (float): Maximum imaginární části.
        n (int): Počet bodů.
        k (int): Maximální počet iterací.

    Return:
        Matice reprezentující Mandelbrotovu množinu.
    """
    x = np.linspace(x_min, x_max, n)
    y = np.linspace(y_min, y_max, n)
    x_realne, y_imaginarni = np.meshgrid(x, y)
    matice_komplexnich_cisel = x_realne + y_imaginarni * 1j
    divergence_matrix = np.zeros((n, n), dtype=int)
    matice_z = np.zeros((n, n), dtype=complex)
    for i in range(k):
        kontrola = np.abs(matice_z) < 2
        matice_z[kontrola] = matice_z[kontrola] ** 2 + matice_komplexnich_cisel[kontrola]
        divergence_matrix = np.where((np.absolute(matice_z) >= 2) & (divergence_matrix == 0), i, divergence_matrix)

    divergence_matrix = np.where(divergence_matrix == 0, k, divergence_matrix)

    return divergence_matrix

def vizualizace_mandelbrot(x_min: float, x_max: float, y_min: float, y_max: float, n: int, k: int):
    """
       Interaktivní vizualizace Mandelbrotovy množiny pomocí matplotlib.
       Funkce využívá pomocné funkce jako je change_cmap která slouží ke změně barevného schématu za využití RadioButtons
        a update, která slouží ke změně vykreslení po změně jednoho ze sliderů(počet iterací, rozsah x_min, x_max, y_min, y_max)

       Args:
           x_min (float): Minimum reálné části.
           x_max (float): Maximum reálné části.
           y_min (float): Minimum imaginární části.
           y_max (float): Maximum imaginární části.
           n (int): Počet bodů.
           k (int): Maximální počet iterací.


       Returns:
           None
       """
    divergence_matrix = mandelbrot_set(x_min, x_max, y_min, y_max, n, k)
    fig, ax = plt.subplots()
    obrazec = plt.imshow(divergence_matrix, cmap='inferno', extent=(x_min, x_max, y_min, y_max))

    ax_iterations = plt.axes([0.20, 0.1, 0.65, 0.03], facecolor='lightgoldenrodyellow')
    it_slider = Slider(ax_iterations, 'Počet iterací', 50, 1000, valinit=k, valstep=1)

    radio_background = 'lightgoldenrodyellow'
    color_map = plt.axes([0.05, 0.4, 0.2, 0.4], facecolor=radio_background)
    cmap_options = ['inferno', 'plasma', 'viridis', 'magma']
    radio = RadioButtons(color_map, cmap_options)

    slider_ax = fig.add_axes([0.20, 0.04, 0.60, 0.03])
    slider_x = RangeSlider(slider_ax, "Osa x", x_min, x_max)
    slider_ay = fig.add_axes([0.20, 0.005, 0.60, 0.03])
    slider_y = RangeSlider(slider_ay, "Osa y", y_min, y_max)


    def change_cmap(label):
        obrazec.set_cmap(label)
        fig.canvas.draw_idle()

    radio.on_clicked(change_cmap)

    ax.set_xlabel('reálná část')
    ax.set_ylabel('imaginární část')
    ax.set_title("Mandelbrotova množina")

    def update(val):
        x_min_update, x_max_update = slider_x.val
        y_min_update, y_max_update = slider_y.val
        k_update = it_slider.val
        divergence_matrix = mandelbrot_set(x_min_update, x_max_update, y_min_update, y_max_update, n, k_update)
        obrazec.set_data(divergence_matrix)
        obrazec.set_extent((x_min_update, x_max_update, y_min_update, y_max_update))
        fig.canvas.draw_idle()

    plt.subplots_adjust(bottom=0.25)
    slider_x.on_changed(update)
    slider_y.on_changed(update)
    it_slider.on_changed(update)
    plt.ion()
    plt.show(block=True)