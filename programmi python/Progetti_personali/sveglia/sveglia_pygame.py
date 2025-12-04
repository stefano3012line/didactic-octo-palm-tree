"""
Sveglia + Pomodoro Timer in Python usando Pygame
Corretto conteggio tempo lavoro reale per il Pomodoro, barra di progresso e alert audio.
"""

import os
import sys
import pygame
from pygame import mixer
from datetime import timedelta

# Config
MUSIC_FOLDER = "music"
WINDOW_SIZE = (1200, 700)
FPS = 30
FONT_SIZE = 24
TITLE = "Sveglia + Pomodoro Timer"
BG_PATH = "background.jpg"
ALERT_SOUND = "alert.mp3"
PROGRESS_BAR_HEIGHT = 20

# Pomodoro settings
WORK_DURATION = 25 * 60
SHORT_BREAK = 5 * 60
LONG_BREAK = 15 * 60
CYCLES_BEFORE_LONG_BREAK = 4

# Utility

def format_td(seconds):
    if seconds < 0:
        seconds = 0
    td = timedelta(seconds=int(seconds))
    mm, ss = divmod(td.seconds, 60)
    hh, mm = divmod(mm, 60)
    if hh:
        return f"{hh:02d}:{mm:02d}:{ss:02d}"
    return f"{mm:02d}:{ss:02d}"


def load_music_list(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    files = []
    for fn in sorted(os.listdir(folder)):
        if fn.lower().endswith((".mp3", ".wav", ".ogg")):
            files.append(os.path.join(folder, fn))
    return files

# Pygame init
pygame.init()
mixer.init()
screen = pygame.display.set_mode(WINDOW_SIZE, pygame.FULLSCREEN)
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, FONT_SIZE)

# State
music_list = load_music_list(MUSIC_FOLDER)
selected_idx = 0
minutes = 0
seconds = 30
countdown_running = False
countdown_paused = False
countdown_start_ticks = None
paused_time_left = None
end_time_ms = None
fullscreen = True
mode = "sveglia"

# Pomodoro state
pomodoro_phase = "work"
pomodoro_cycle_count = 0
total_work_seconds = 0
pomodoro_timer = 0
pomodoro_phase_duration = WORK_DURATION
pomodoro_elapsed = 0  # tempo reale trascorso nella fase corrente

# Functions

def draw_text(surface, text, pos, align="topleft"):
    r = font.render(text, True, (255, 255, 255))
    rect = r.get_rect()
    setattr(rect, align, pos)
    surface.blit(r, rect)


def draw_progress_bar(surface, x, y, width, height, progress):
    pygame.draw.rect(surface, (100, 100, 100), (x, y, width, height))
    pygame.draw.rect(surface, (0, 200, 0), (x, y, width * progress, height))


def start_countdown(total_seconds):
    global countdown_running, countdown_start_ticks, paused_time_left, countdown_paused, end_time_ms
    countdown_running = True
    countdown_paused = False
    paused_time_left = None
    countdown_start_ticks = pygame.time.get_ticks()
    end_time_ms = countdown_start_ticks + int(total_seconds * 1000)


def stop_music():
    try:
        mixer.music.stop()
    except Exception:
        pass


def play_music(path):
    try:
        mixer.music.load(path)
        mixer.music.play(-1)
    except Exception as e:
        print("Errore riproduzione musica:", e)


def play_alert():
    try:
        alert = mixer.Sound(ALERT_SOUND)
        alert.play()
    except Exception as e:
        print("Errore riproduzione alert:", e)


def toggle_fullscreen():
    global screen, fullscreen
    fullscreen = not fullscreen
    if fullscreen:
        screen = pygame.display.set_mode(WINDOW_SIZE, pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode(WINDOW_SIZE)

# Main loop
running = True
while running:
    dt = clock.tick(FPS) / 1000.0  # secondi trascorsi

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                toggle_fullscreen()
            elif event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_UP:
                if music_list:
                    selected_idx = (selected_idx - 1) % len(music_list)
            elif event.key == pygame.K_DOWN:
                if music_list:
                    selected_idx = (selected_idx + 1) % len(music_list)
            elif event.key == pygame.K_RIGHT:
                if mode == "sveglia":
                    minutes += 1
                elif mode == "pomodoro":
                    pomodoro_timer += 60
                    pomodoro_phase_duration += 60
            elif event.key == pygame.K_LEFT:
                if mode == "sveglia":
                    minutes = max(0, minutes - 1)
                elif mode == "pomodoro":
                    pomodoro_timer = max(1, pomodoro_timer - 60)
                    pomodoro_phase_duration = max(1, pomodoro_phase_duration - 60)
            elif event.key == pygame.K_PAGEUP:
                if mode == "sveglia":
                    seconds = min(59, seconds + 5)
            elif event.key == pygame.K_PAGEDOWN:
                if mode == "sveglia":
                    seconds = max(0, seconds - 5)
            elif event.key == pygame.K_RETURN:
                if mode == "sveglia":
                    total = minutes * 60 + seconds
                    if total > 0:
                        start_countdown(total)
                        stop_music()
            elif event.key == pygame.K_SPACE:
                if mode == "pomodoro":
                    countdown_paused = not countdown_paused
                else:
                    if countdown_running and not countdown_paused:
                        countdown_paused = True
                        now = pygame.time.get_ticks()
                        remaining_ms = max(0, end_time_ms - now) if end_time_ms else 0
                        paused_time_left = remaining_ms / 1000.0
                    elif countdown_running and countdown_paused:
                        countdown_paused = False
                        if paused_time_left is not None:
                            end_time_ms = pygame.time.get_ticks() + int(paused_time_left * 1000)
                            paused_time_left = None
            elif event.key == pygame.K_s:
                stop_music()
            elif event.key == pygame.K_r:
                countdown_running = False
                countdown_paused = False
                end_time_ms = None
                paused_time_left = None
                stop_music()
            elif event.key == pygame.K_p:
                mode = "pomodoro"
                pomodoro_phase = "work"
                pomodoro_timer = WORK_DURATION
                pomodoro_phase_duration = WORK_DURATION
                pomodoro_elapsed = 0
                countdown_paused = False
            elif event.key == pygame.K_a:
                mode = "sveglia"
                countdown_running = False
                countdown_paused = False
                end_time_ms = None
                paused_time_left = None
                stop_music()

    # Background
    try:
        bg = pygame.image.load(BG_PATH)
        bg = pygame.transform.scale(bg, screen.get_size())
        screen.blit(bg, (0, 0))
    except Exception:
        screen.fill((35, 40, 48))

    # Update display
    if mode == "sveglia":
        draw_text(screen, f"Modalità: Sveglia", (20, 10))
        draw_text(screen, f"Imposta tempo: Minuti {minutes}, Secondi {seconds}", (20, 50))
        if countdown_running:
            remaining = paused_time_left if countdown_paused else max(0, (end_time_ms - pygame.time.get_ticks()) / 1000.0)
            draw_text(screen, "Countdown: " + format_td(remaining), (20, 100))
            if remaining <= 0:
                countdown_running = False
                stop_music()

    elif mode == "pomodoro":
        draw_text(screen, f"Modalità: Pomodoro - Fase: {pomodoro_phase}", (20, 10))
        if not countdown_paused:
            pomodoro_timer -= dt
            pomodoro_elapsed += dt
        draw_text(screen, f"Timer: {format_td(pomodoro_timer)}", (20, 50))
        draw_text(screen, f"Cicli completati: {pomodoro_cycle_count}", (20, 80))
        draw_text(screen, f"Tempo totale lavoro: {format_td(total_work_seconds)}", (20, 110))

        progress = max(0, min(1, 1 - pomodoro_timer / pomodoro_phase_duration))
        draw_progress_bar(screen, 20, 140, screen.get_width() - 40, PROGRESS_BAR_HEIGHT, progress)

        if pomodoro_timer <= 0:
            play_alert()
            if pomodoro_phase == "work":
                total_work_seconds += int(pomodoro_elapsed)
                pomodoro_cycle_count += 1
                if pomodoro_cycle_count % CYCLES_BEFORE_LONG_BREAK == 0:
                    pomodoro_phase = "long_break"
                    pomodoro_timer = LONG_BREAK
                    pomodoro_phase_duration = LONG_BREAK
                else:
                    pomodoro_phase = "short_break"
                    pomodoro_timer = SHORT_BREAK
                    pomodoro_phase_duration = SHORT_BREAK
            else:
                pomodoro_phase = "work"
                pomodoro_timer = WORK_DURATION
                pomodoro_phase_duration = WORK_DURATION
            pomodoro_elapsed = 0

    draw_text(screen, "INVIO: start/stop Sveglia   SPACE: pausa/riprendi Pomodoro   P: Pomodoro   A: Sveglia   S: stop musica   FRECCE: regola tempo   F11: fullscreen   PAG: secondi", (20, screen.get_height()-40))

    pygame.display.flip()