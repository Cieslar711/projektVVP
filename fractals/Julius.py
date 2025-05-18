import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider,RadioButtons, RangeSlider

matplotlib.use('TkAgg')

def julius_set(c: complex, x_min: float, x_max: float, y_min: float, y_max: float, n: int, k: int):
    """
     Vypočítá Juliovu množinu pro danou konstantu c.

     Args:
         c (complex): Komplexní konstanta.
         x_min (float): Minimum reálné části.
         x_max (float): Maximum reálné části.
         y_min (float): Minimum imaginární části.
         y_max (float): Maximum imaginární části.
         n (int): Počet bodů.
         k (int): Počet iterací.

     Returns:
         Matice reprezentující Juliovu množinu.
     """
    x = np.linspace(x_min, x_max, n)
    y = np.linspace(y_min, y_max, n)
    x_realne, y_imaginarni = np.meshgrid(x, y)
    matice_komplexnich_cisel = x_realne + y_imaginarni * 1j
    divergence_matrix = np.zeros((n, n), dtype=int)

    for i in range(k):
        kontrola = np.abs(matice_komplexnich_cisel) < 2
        matice_komplexnich_cisel[kontrola] = matice_komplexnich_cisel[kontrola] ** 2 + c
        divergence_matrix = np.where((np.absolute(matice_komplexnich_cisel) >= 2) & (divergence_matrix == 0), i, divergence_matrix)

    divergence_matrix = np.where(divergence_matrix == 0, k, divergence_matrix)

    return divergence_matrix


def vizualizace_julius(c: complex, x_min: float, x_max: float, y_min: float, y_max: float, n: int, k: int):
    """
       Interaktivní vizualizace Juliovy množiny pomocí matplotlib.

       Args:
           c (complex): Komplexní konstanta.
           x_min (float): Minimum reálné části.
           x_max (float): Maximum reálné části.
           y_min (float): Minimum imaginární části.
           y_max (float): Maximum imaginární části.
           n (int): Počet bodů.
           k (int): Maximální počet iterací.

       Function:
           change_cmap - slouží ke změně barevného schématu za využití RadioButtons z knihovny matplotlib.widgets
           update -  slouží ke změně vykreslení po změně jednoho ze sliderů(počet iterací, rozsah x_min, x_max, y_min, y_max, komplexní konstanta c)


       Returns:
           None
       """
    divergence_matrix = julius_set(c, x_min, x_max, y_min, y_max, n, k)
    init_real = 0.285
    init_imag = 0.01
    c_init = complex(init_real, init_imag)
    fig, ax = plt.subplots()
    ax.set_xlabel('reálná část')
    ax.set_ylabel('imaginární část')
    ax.set_title("Juliova množina")
    plt.subplots_adjust(bottom = 0.25)
    obrazec = ax.imshow(divergence_matrix, cmap='twilight', extent=(x_min, x_max, y_min, y_max))

    ax_real = plt.axes([0.20, 0.18, 0.65, 0.03], facecolor='lightgoldenrodyellow')
    real_slider = Slider(ax_real, 'Reálná část', x_min, x_max, valinit=c.real)

    ax_imag = plt.axes([0.20, 0.13, 0.65, 0.03], facecolor='lightgoldenrodyellow')
    imag_slider = Slider(ax_imag, 'Imaginární část', y_min, y_max, valinit=c.imag)

    ax_iterations = plt.axes([0.20, 0.08, 0.65, 0.03], facecolor='lightgoldenrodyellow')
    it_slider = Slider(ax_iterations, 'Počet iterací', 50, 1000, valinit=k, valstep=1)

    slider_ax = fig.add_axes([0.20, 0.03, 0.60, 0.03])
    slider_x = RangeSlider(slider_ax, "Osa x", x_min, x_max)
    slider_ay = fig.add_axes([0.20, 0.00, 0.60, 0.03])
    slider_y = RangeSlider(slider_ay, "Osa y", y_min, y_max)

    radio_background = 'lightgoldenrodyellow'
    color_map = plt.axes([0.05, 0.4, 0.2, 0.4], facecolor=radio_background)
    cmap_options = ['inferno', 'plasma', 'viridis', 'magma']
    radio = RadioButtons(color_map, cmap_options)

    def change_cmap(label):
        obrazec.set_cmap(label)
        fig.canvas.draw_idle()

    radio.on_clicked(change_cmap)

    def update(val):
        c = complex(real_slider.val, imag_slider.val)
        x_min_update, x_max_update = slider_x.val
        y_min_update, y_max_update = slider_y.val
        k_update = it_slider.val
        divergence_matrix = julius_set(c, x_min_update, x_max_update, y_min_update, y_max_update, n, k_update)
        obrazec.set_data(divergence_matrix)
        fig.canvas.draw_idle()

    real_slider.on_changed(update)
    imag_slider.on_changed(update)
    slider_x.on_changed(update)
    slider_y.on_changed(update)
    it_slider.on_changed(update)
    plt.subplots_adjust(bottom=0.3)
    plt.ion()
    plt.show(block=True)