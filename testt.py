import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import display, clear_output
import ipywidgets as widgets


# Parámetros
t_start = 0
t_end = 5
n_points = 250
timestep = (t_end - t_start) / n_points
t = np.linspace(t_start, t_end, n_points)

g = -9.81*5
vx = 1

x0 = 0
y0 = 10.0
vy0 = 0
r0 = [x0, y0, vy0]

# Estado global para el control
u_frame = [False]  # Se activa solo para el frame actual

def control_u(x, y, vy):
    # Si u_frame está True, aplicar impulso SOLO para este frame
    if u_frame[0]:
        u = -g - vy / timestep+500
    else:
        u = 0
    return u

def dynamics(r, t, g, vx):
    x, y, vy = r
    drdt = [vx, vy, g + control_u(x, y, vy)]
    return drdt

# Interfaz para activar u SOLO para el frame actual con la barra espaciadora
def on_key_press(event):
    if event.key == ' ':
        u_frame[0] = True  # Se activa solo para el siguiente frame

# Nota: No necesitamos on_key_release, ya que el flag se limpia en cada frame

# Inicialización
solution = np.zeros((n_points, 3))
solution[0] = r0

fig, ax = plt.subplots(figsize=(10, 5))
line, = ax.plot([], [], '*', label='trayectoria')
point, = ax.plot([], [], 'ro')
ax.set_xlim(0, vx * t_end + 1)
ax.set_ylim(0, y0 + 2)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.legend()
plt.tight_layout()

# Para guardar la trayectoria en tiempo real
x_data = []
y_data = []

def init():
    line.set_data([], [])
    point.set_data([], [])
    return line, point

def animate(i):
    if i == 0:
        x_data.clear()
        y_data.clear()
        solution[0] = r0
    else:
        r_prev = solution[i-1]
        t_prev = t[i-1]
        drdt = dynamics(r_prev, t_prev, g, vx)
        solution[i] = r_prev + np.array(drdt) * timestep
    x = solution[i, 0]
    y = solution[i, 1]
    x_data.append(x)
    y_data.append(y)
    line.set_data(x_data, y_data)
    point.set_data([x], [y])
    # Limpiar el flag después de cada frame, así solo dura un frame
    u_frame[0] = False
    return line, point

# Conectar eventos de teclado
cid_press = fig.canvas.mpl_connect('key_press_event', on_key_press)
# No necesitamos key_release

# Animación
ani = FuncAnimation(fig, animate, frames=n_points, init_func=init, interval=20, blit=True, repeat=False)

plt.show()
