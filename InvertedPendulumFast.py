import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import imageio.v2 as imageio
import os
import math
import PySimpleGUI as sG
import threading
import multiprocessing as mp

if __name__ == '__main__':

    sG.theme('DarkGrey2')   # ustawienie koloru okna

    col1 = [[sG.Text("Kąt początkowy pierwszej")],
            [sG.Text("Długość ramienia:")],
            [sG.Text("Amplituda drgań punktu:")],
            [sG.Text("Częstotliwość drgań:")],
            [sG.Text("Przyspieszenie ziemskie:")],
            [sG.Text("Klatkaż animacji:")],
            [sG.Text("Czas animacji:")],
            [sG.Text("Kolor masy:")],
            [sG.Text("Rysowanie śladu masy:")]]


    col2 = [[sG.Input(default_text=85)],  # value 0 kąt
            [sG.Input(default_text=1)],  # value 1 ramię
            [sG.Input(default_text=0.05)],  # value 2 amplituda
            [sG.Input(default_text=20)],  # value 3 Hz
            [sG.Input(default_text=9.81)],  # value 4 g
            [sG.Input(default_text=30)],  # value 5 fps
            [sG.Input(default_text=5)],  # value 6 s
            [sG.Combo(["Czerwony", "Zielony", "Niebieski", "Żółty                                     "], default_value="Czerwony", key="kolor")],  # kolor value7
            [sG.Checkbox("Tak", key="slad", default=True)]]  # slad value 8


    col3 = [[sG.Text("stopni")],
            [sG.Text("m")],
            [sG.Text("m")],
            [sG.Text("Hz")],
            [sG.Text("m/s^2")],
            [sG.Text("FPS")],
            [sG.Text("s")],
            [sG.Text("")],
            [sG.Text("")]]

    layout = [[sG.Column(col1), sG.Column(col2), sG.Column(col3)],
            [sG.Button("   Symulacja   ")],
            [sG.Output(size=(82, 5))]]

    window = sG.Window("Symulator wahadła odwróconego", layout, element_justification="center")  # tworzenie okna

def make_plot(i):
    # Renderuje i zapiuje klatkę chwilowego położenia mas i prętów w chwili i
    ax.plot([0, x1[i]], [y_zaczep[i], y1[i] + y_zaczep[i]], lw=2, c='k')
    # Kulki kolejno punktu kotwiczenia, masy 1 i masy 2
    c0 = Circle((0, y_zaczep[i]), 0.05 / 2, fc='k', zorder=10)
    c1 = Circle((x1[i], y1[i] + y_zaczep[i]), r, fc=kolor, ec=kolor, zorder=10)
    ax.add_patch(c0)
    ax.add_patch(c1)

    # Slad jest podzielony na ns segmentów i cieniowany aby znikał po pewnym czasie
    ns = 20
    s = max_trail // ns

    if slad == True:
        for j in range(ns):
            imin = int(i - (ns - j) * s)
            if imin < 0:
                continue
            imax = int(imin + s + 1)
            
            # Ślad wygląda lepiej jeśli podniesiemy (j/ns) do kwadratu
            alpha = (j / ns) ** 2
            ax.plot(x1[imin:imax], y1[imin:imax] + y_zaczep[imin:imax], c=kolor, solid_capstyle='butt', lw=2, alpha=alpha)
        
    # Wyśrodkowanie obrazka i wyrównanie osi żeby były identyczne
    ax.set_xlim(-l - r - A, l + r + A)
    ax.set_ylim(-l - r - A, l + r + A)
    ax.set_aspect('equal', adjustable='box')
    plt.axis('off')
    plt.savefig('frames/_img{:04d}.png'.format(i), dpi=72)
    plt.cla()

def get_data():
    global A, ax, max_trail, slad, x1, y1, kolor, frq, fps, l, r, y_zaczep
    with open("data.txt", "r") as file:
        data = []
        i=0
        for line in file:
            i += 1
            if i == 10:
                data.append(str(line.strip()))
                break
            try:
                data.append(float(line.strip()))
            except:
                data.append(bool(line.strip()))
    alfa_start = int(data[0])
    l = data[1]
    A = data[2]
    frq = data[3]
    g = data[4]
    fps = data[5]
    tmax = int(data[6])
    slad = data[7]
    dt = 1/fps
    def deriv(y, t, l):
        # Zwraca pochodne y = phi, z

        phi, z = y

        phidot = z
        zdot = -1 * (1/l) * (g + A * (2 * np.pi * frq) ** 2 * np.cos(2 * np.pi * frq * t)) * np.sin(phi)

        return phidot, zdot
    t = np.arange(0, tmax, dt)
    y0 = np.array([math.radians(alfa_start) + np.pi / 2, 0])
    y = odeint(deriv, y0, t, args=(l, ))
    phi = y[:, 0]
    x1 = l * np.sin(phi)
    y1 = -l * np.cos(phi)
    max_trail = 1 / dt
    fig = plt.figure(figsize=(10, 10), dpi=72)
    ax = fig.add_subplot(111)
    kolor = data[9]
    r = 0.05
    y_zaczep = A * np.sin(2 * np.pi * frq * t)


def wahadlo():

#    try:
    global A, ax, max_trail, slad, x1, y1, kolor, frq, fps, l, r
    alfa_start = int(values[0])

    # L - długości ramienia wahadła (m)
    l = float(values[1])
    A = float(values[2])
    frq = float(values[3])

    # Przyspieszenie grawitacyjne (m/s^2)
    g = float(values[4])

    # Klatkaż animacji
    fps = int(values[5])

    # tmax - czas animacji (s)
    # dt - odstępy czasowe (s)
    tmax = int(values[6])
    dt = 1/fps

    data_list = [alfa_start, l, A, frq, g, fps, tmax]

    # s decyduje czy rysować ślady masy m
    slad = values["slad"]

    

    # Promień rysowanych kulek uzaleznione od mas i kolory mas 1 i 2
    r = 0.05

    if values["kolor"] == "Czerwony":
        kolor = "r"
    elif values["kolor"] == "Zielony":
        kolor = "g"
    elif values["kolor"] == "Niebieski":
        kolor = "b"
    elif values["kolor"] == "Żółty                                     ":
        kolor = "y"


    # Rysuje ślad masy m dla ostatnich trail_secs sekund
    trail_secs = 1
    try: #Możliwe że do wyjebania jeśli będziemy używać MP4
        current_directory = os.getcwd() 
        final_directory = os.path.join(current_directory, r'frames')
        if not os.path.exists(final_directory):
            os.makedirs(final_directory)
    except OSError:
        print("Nie udało się stworzyć folderu")


    def deriv(y, t, l):
        # Zwraca pochodne y = phi, z

        phi, z = y

        phidot = z
        zdot = -1 * (1/l) * (g + A * (2 * np.pi * frq) ** 2 * np.cos(2 * np.pi * frq * t)) * np.sin(phi)

        return phidot, zdot


    t = np.arange(0, tmax, dt)

    with open("data.txt", "w") as file:
        for item in data_list:
            file.write(str(item) + "\n")
        file.write(str(slad) + "\n")
        file.write(str(kolor))
    # Początkowe warunki: kąty startowe alfa zdefiniowane przez użytkownika i pochodne = 0
    y0 = np.array([math.radians(alfa_start) + np.pi / 2, 0])

    # Numeryczne całkowanie równań ruchu
    y = odeint(deriv, y0, t, args=(l, ))

    # z i phi w funkcji czasu
    phi = y[:, 0]

    # Zamiana na współrzędne kartezjańskie położeń obu mas
    x1 = l * np.sin(phi)
    y1 = -l * np.cos(phi)
    # Maksymalna ilość punktów rysowanego śladu
    max_trail = trail_secs / dt

    fig = plt.figure(figsize=(10, 10), dpi=72)
    ax = fig.add_subplot(111)

    mp4_writing = imageio.get_writer('Animacja.mp4', fps = fps, codec='libx264')

    with mp.Pool(processes=mp.cpu_count()) as pool:
        pool.map(make_plot, range(0, t.size))
    
    for i in range(0, t.size):
        print("Renderowanie klatek", i + 1, 'z', t.size)
        window.refresh()
        frame = imageio.imread('frames/_img{:04d}.png'.format(i))
        mp4_writing.append_data(frame)
        os.remove('frames/_img{:04d}.png'.format(i))
    
    mp4_writing.close()
    

    print("Proces zakończony sukcesem, utworzono animację wideo MP4")
    try:
        os.startfile('Animacja.mp4')
    except:
        print("Nie można uruchomić animacji automatycznie, spróbuj zrobić to ręcznie z folderu frames")

    print("Możesz zmienić dane i wykonać symulację kolejny raz")
    return 0

  #  except:
   #     print("Podano złe dane, spróbuj jeszcze raz")
    #    return 0


if __name__ == '__main__':
    while True:
        event, values = window.read()
        if event == sG.WIN_CLOSED:  # jeżeli uzytkownik zamyka okno
            break
        wahadlo()
else:
    get_data()

