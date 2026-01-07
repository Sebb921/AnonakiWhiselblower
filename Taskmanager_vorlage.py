import pygame
import psutil
import sys
import time

# -------------------- Initialisierung --------------------
pygame.init()

WIDTH, HEIGHT = 900, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("System Monitor – Simple")

clock = pygame.time.Clock()

# Farben
BG = (15, 15, 25)
ACCENT = (0, 200, 180)
WHITE = (220, 220, 220)
GRAY = (140, 140, 160)
BAR_BG = (40, 40, 60)

# Schrift
font_title = pygame.font.SysFont("consolas", 28, bold=True)
font = pygame.font.SysFont("consolas", 20)

# -------------------- Hilfsfunktionen --------------------
def draw_text(text, x, y, color=WHITE):
    screen.blit(font.render(text, True, color), (x, y))

def draw_bar(x, y, w, h, percent):
    pygame.draw.rect(screen, BAR_BG, (x, y, w, h))
    pygame.draw.rect(screen, ACCENT, (x, y, int(w * percent / 100), h))
    pygame.draw.rect(screen, WHITE, (x, y, w, h), 2)

def format_uptime(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

# -------------------- Hauptloop --------------------
running = True
last_update = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_q):
                running = False

    # Werte alle 1 Sekunde aktualisieren
    if time.time() - last_update >= 1:
        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        net = psutil.net_io_counters()
        battery = psutil.sensors_battery()
        uptime = time.time() - psutil.boot_time()
        process_count = len(psutil.pids())

        last_update = time.time()

    # -------------------- Rendering --------------------
    screen.fill(BG)

    draw_text("SYSTEM MONITOR", 20, 20, ACCENT)

    y = 80

    # CPU
    draw_text(f"CPU-Auslastung: {cpu:.1f}%", 20, y)
    draw_bar(20, y + 30, 860, 20, cpu)
    y += 70

    # RAM
    used_ram = mem.used / (1024 ** 3)
    total_ram = mem.total / (1024 ** 3)
    draw_text(f"RAM: {used_ram:.1f} / {total_ram:.1f} GB ({mem.percent:.1f}%)", 20, y)
    draw_bar(20, y + 30, 860, 20, mem.percent)
    y += 70

    # Datenträger
    used_disk = disk.used / (1024 ** 3)
    total_disk = disk.total / (1024 ** 3)
    disk_percent = disk.percent
    draw_text(f"Datenträger: {used_disk:.1f} / {total_disk:.1f} GB ({disk_percent:.1f}%)", 20, y)
    draw_bar(20, y + 30, 860, 20, disk_percent)
    y += 70

    # Akku
    if battery:
        status = "Netzbetrieb" if battery.power_plugged else "Akku"
        draw_text(f"Akku: {battery.percent:.1f}% ({status})", 20, y)
        draw_bar(20, y + 30, 860, 20, battery.percent)
    else:
        draw_text("Akku: Nicht verfügbar", 20, y, GRAY)
    y += 70

    # Netzwerk
    down_mb = net.bytes_recv / (1024 ** 2)
    up_mb = net.bytes_sent / (1024 ** 2)
    draw_text(f"Netzwerk ↓ {down_mb:.1f} MB   ↑ {up_mb:.1f} MB", 20, y)
    y += 40

    # Uptime + Prozesse
    draw_text(f"System-Uptime: {format_uptime(uptime)}", 20, y)
    y += 30
    draw_text(f"Aktive Prozesse: {process_count}", 20, y)

    draw_text("ESC oder Q zum Beenden", 20, HEIGHT - 40, GRAY)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
