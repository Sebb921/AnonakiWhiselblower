import pygame
import psutil
import sys
import time
from datetime import datetime
 
# pygame initialisieren
pygame.init()
 
# Fenster-Einstellungen
WIDTH, HEIGHT = 1000, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("System-Monitor Live – Pygame Edition")
clock = pygame.time.Clock()
 
# Farben (Cyberpunk/Dark Theme)
BG = (10, 12, 18)
ACCENT = (0, 255, 200)
ACCENT2 = (255, 0, 200)
WHITE = (220, 220, 220)
GRAY = (100, 100, 120)
BAR_BG = (30, 30, 45)
BAR_FILL = (0, 220, 180)
 
# Schriftarten
font_big = pygame.font.SysFont("consolas", 28, bold=True)
font_med = pygame.font.SysFont("consolas", 22)
font_small = pygame.font.SysFont("consolas", 18)
font_tiny = pygame.font.SysFont("consolas", 16)
 
def draw_text(text, font, color, x, y, align="left"):
    surf = font.render(text, True, color)
    rect = surf.get_rect()
    if align == "left":
        rect.topleft = (x, y)
    elif align == "center":
        rect.midtop = (x, y)
    screen.blit(surf, rect)
 
def draw_bar(x, y, w, h, percent, text=""):
    pygame.draw.rect(screen, BAR_BG, (x, y, w, h))
    fill_w = int(w * percent / 100) #Berechnet, wie viele Pixel gefüllt werden, abhängig CPU
    pygame.draw.rect(screen, BAR_FILL, (x, y, fill_w, h))
    pygame.draw.rect(screen, ACCENT, (x, y, w, h), 2)
    if text:
        draw_text(text, font_small, WHITE, x + w//2, y + 6, "center")
 
def get_top_processes(n=10):
    process_info = []
 
    #Schaut alle laufenden Prozesse an und fordert nur diese vier Infos
    for process in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            process_info.append(process.info)
        except:
            pass
    return sorted(process_info, key=lambda x: x['cpu_percent'] or 0, reverse=True)[:n]
 
# Hauptloop
running = True
last_update = 0
 
while running:
    current_time = time.time()
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                running = False
 
    # Update alle 2 Sekunden
    if current_time - last_update >= 2.0:
        # Daten sammeln
        cpu_percent = psutil.cpu_percent(interval=None)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        net = psutil.net_io_counters()
        top_process_info = get_top_processes(10)
        last_update = current_time
 
    # Hintergrund
    screen.fill(BG)
 
    y = 20
 
    # Titel
    draw_text("SYSTEM-MONITOR LIVE", font_big, ACCENT, WIDTH//2, y, "center")
    draw_text(f"Aktualisiert: {datetime.now().strftime('%H:%M:%S')}", font_small, GRAY, WIDTH//2, y+40, "center")
    y += 100
 
    # CPU
    draw_text("CPU", font_med, ACCENT, 40, y)
    y += 40
    draw_text(f"Gesamtnutzung: {cpu_percent:6.1f}%", font_med, WHITE, 60, y)
    draw_bar(60, y+40, 880, 30, cpu_percent, f"{cpu_percent:.1f}%")
    y += 90
 
    # Top 5 CPU-Prozesse
    draw_text("Top 5 Prozesse (CPU)", font_med, ACCENT2, 40, y)
    y += 40
    for i, p in enumerate(get_top_processes(5)):
        name = (p['name'][:30] + '..') if len(p['name']) > 30 else p['name']
        txt = f"{p['pid']:>6}  {name:<32} {p['cpu_percent']:6.1f}%"
        draw_text(txt, font_small, WHITE if i < 3 else GRAY, 60, y + i*28)
    y += 180
 
    # RAM
    draw_text("Arbeitsspeicher (RAM)", font_med, ACCENT, 40, y)
    y += 40
    used_gb = mem.used / (1024**3)
    total_gb = mem.total / (1024**3)
    draw_text(f"Verbraucht: {used_gb:.1f} GB von {total_gb:.1f} GB ({mem.percent:.1f}%)", font_small, WHITE, 60, y)
    draw_bar(60, y+35, 880, 30, mem.percent, f"{mem.percent:.1f}%")
    y += 100
 
    # Festplatte
    draw_text("Datenträger (/) ", font_med, ACCENT, 40, y)
    y += 40
    disk_used_gb = disk.used / (1024**3)
    disk_total_gb = disk.total / (1024**3)
    disk_perc = disk.used / disk.total * 100
    draw_text(f"Belegt: {disk_used_gb:.1f} GB von {disk_total_gb:.1f} GB ({disk_perc:.1f}%)", font_small, WHITE, 60, y)
    draw_bar(60, y+35, 880, 30, disk_perc, f"{disk_perc:.1f}%")
    y += 100
 
    # Netzwerk
    draw_text("Netzwerkverkehr (seit Boot)", font_med, ACCENT, 40, y)
    y += 40
    down_mb = net.bytes_recv / (1024**2)
    up_mb = net.bytes_sent / (1024**2)
    draw_text(f"Eingehend: {down_mb:9.1f} MB", font_small, WHITE, 60, y)
    draw_text(f"Ausgehend:  {up_mb:9.1f} MB", font_small, WHITE, 60, y+30)
    y += 100
 
    # Top 10 Prozesse Tabelle
    draw_text("Top 10 Prozesse nach CPU-Nutzung", font_med, ACCENT2, 40, y)
    y += 40
 
    headers = ["PID", "Prozessname", "CPU%", "RAM%"]
    col_x = [60, 160, 560, 700]
    for i, h in enumerate(headers):
        draw_text(h, font_small, ACCENT, col_x[i], y)
    pygame.draw.line(screen, ACCENT, (60, y+25), (940, y+25), 2)
    y += 40
 
    for i, p in enumerate(top_process_info):
        name = (p['name'][:35] + '..') if len(p['name']) > 35 else p['name']
        color = WHITE if i < 3 else GRAY
        draw_text(str(p['pid']), font_tiny, color, col_x[0], y + i*26)
        draw_text(name, font_tiny, color, col_x[1], y + i*26)
        draw_text(f"{p['cpu_percent']:5.1f}%", font_tiny, color, col_x[2], y + i*26)
        draw_text(f"{p['memory_percent']:5.1f}%", font_tiny, color, col_x[3], y + i*26)
 
    # Footer
    draw_text("Drücke Q oder ESC zum Beenden", font_small, GRAY, WIDTH//2, HEIGHT - 40, "center")
 
    pygame.display.flip()
    clock.tick(30)  # max 30 FPS – reicht völlig für Monitoring
 
pygame.quit()
sys.exit()