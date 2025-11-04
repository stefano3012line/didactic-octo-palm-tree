import pygame
import random
import math
from dataclasses import dataclass
from typing import List, Tuple
from enum import Enum

# Configurazione
WIDTH, HEIGHT = 1200, 800
FPS = 30
GRID_SIZE = 10

# Colori
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 139, 34)
LIGHT_GREEN = (144, 238, 144)
BROWN = (139, 69, 19)
YELLOW = (255, 215, 0)
RED = (220, 20, 60)
BLUE = (70, 130, 180)

class EntityType(Enum):
    PLANT = 1
    HERBIVORE = 2
    PREDATOR = 3

@dataclass
class Stats:
    """Statistiche dell'ecosistema"""
    plants: int = 0
    herbivores: int = 0
    predators: int = 0
    generation: int = 0

class Entity:
    """Classe base per tutte le entità"""
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.alive = True

    def update(self, ecosystem):
        pass

    def draw(self, screen):
        pass

    def distance_to(self, other) -> float:
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

class Plant(Entity):
    """Pianta - cresce nel tempo e può riprodursi"""
    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        self.energy = 30
        self.max_energy = 100
        self.growth_rate = 0.5
        self.reproduction_threshold = 80
        self.reproduction_cooldown = 0
        self.size = 4

    def update(self, ecosystem):
        # Crescita
        if self.energy < self.max_energy:
            self.energy += self.growth_rate
            self.size = 4 + (self.energy / self.max_energy) * 4

        # Riproduzione
        self.reproduction_cooldown -= 1
        if self.energy >= self.reproduction_threshold and self.reproduction_cooldown <= 0:
            if random.random() < 0.05:  # 5% chance per frame
                self.reproduce(ecosystem)
                self.reproduction_cooldown = 100

    def reproduce(self, ecosystem):
        # Spawn nuova pianta nelle vicinanze
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(20, 50)
        new_x = self.x + math.cos(angle) * distance
        new_y = self.y + math.sin(angle) * distance

        if 0 < new_x < WIDTH and 0 < new_y < HEIGHT:
            new_plant = Plant(new_x, new_y)
            ecosystem.plants.append(new_plant)
            self.energy -= 20

    def draw(self, screen):
        color_intensity = int(100 + (self.energy / self.max_energy) * 155)
        color = (0, color_intensity, 0)
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), int(self.size))

class Animal(Entity):
    """Classe base per animali"""
    def __init__(self, x: float, y: float, color, speed, vision_range):
        super().__init__(x, y)
        self.color = color
        self.speed = speed
        self.vision_range = vision_range
        self.energy = 100
        self.max_energy = 150
        self.age = 0
        self.max_age = 1000
        self.reproduction_threshold = 120
        self.size = 6
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)

    def move(self):
        """Movimento base con variazione casuale"""


        # Aggiungi variazione casuale alla direzione
        self.vx += random.uniform(-0.3, 0.3)
        self.vy += random.uniform(-0.3, 0.3)

        # Normalizza velocità
        vel = math.sqrt(self.vx**2 + self.vy**2)

        if vel > 0:
            self.vx = (self.vx / vel) * self.speed
            self.vy = (self.vy / vel) * self.speed
        elif vel == 0:
            # 💡 CORREZIONE: Se è completamente fermo (vel=0), dagli una spinta casuale
            self.vx = random.uniform(-1, 1) * self.speed
            self.vy = random.uniform(-1, 1) * self.speed


        # Muovi
        self.x += self.vx
        self.y += self.vy

        # Rimbalza sui bordi
        if self.x < 0 or self.x > WIDTH:
            self.vx *= -1
            self.x = max(0, min(WIDTH, self.x))
        if self.y < 0 or self.y > HEIGHT:
            self.vy *= -1
            self.y = max(0, min(HEIGHT, self.y))

    def seek_target(self, target):
        """Muovi verso un target"""
        if target:
            dx = target.x - self.x
            dy = target.y - self.y
            dist = math.sqrt(dx**2 + dy**2)
            if dist > 0:
                self.vx = (dx / dist) * self.speed
                self.vy = (dy / dist) * self.speed

    def find_nearest(self, entities, max_distance=None):
        """Trova l'entità più vicina"""
        nearest = None
        min_dist = max_distance if max_distance else float('inf')

        for entity in entities:
            if entity.alive:
                dist = self.distance_to(entity)
                if dist < min_dist:
                    min_dist = dist
                    nearest = entity

        return nearest

    def update(self, ecosystem):
        self.age += 1
        self.energy -= 0.15  # Consumo energetico base

        # Morte per età o fame
        if self.age >= self.max_age or self.energy <= 0:
            self.alive = False

    def draw(self, screen):
        # Corpo
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        # Indicatore direzione
        end_x = self.x + self.vx * 3
        end_y = self.y + self.vy * 3
        pygame.draw.line(screen, BLACK, (int(self.x), int(self.y)),
                        (int(end_x), int(end_y)), 2)

class Herbivore(Animal):
    """Erbivoro - mangia piante"""
    def __init__(self, x: float, y: float):
        super().__init__(x, y, YELLOW, speed=2, vision_range=80)
        self.max_age = 800

    def update(self, ecosystem):
        super().update(ecosystem)

        if not self.alive:
            return

        # 1. Movimento di base/casuale
        self.move()

        # 2. Cerca piante (priorità)
        nearest_plant = self.find_nearest(ecosystem.plants, self.vision_range)

        if nearest_plant and nearest_plant.alive:
            dist = self.distance_to(nearest_plant)

            if dist < 15:  # Abbastanza vicino per mangiare
                # Quando è vicino, NON chiamare seek_target per evitare oscillazioni
                # Ma non fermare i vettori vx/vy: l'animale continua ad oscillare leggermente
                eat_amount = min(30, nearest_plant.energy)
                self.energy += eat_amount
                nearest_plant.energy -= eat_amount
                if nearest_plant.energy <= 0:
                    nearest_plant.alive = False
            else:
                # Se il bersaglio è in vista ma lontano, muovi verso di esso
                self.seek_target(nearest_plant)
        # Riproduzione
        if self.energy >= self.reproduction_threshold and random.random() < 0.003:
            self.reproduce(ecosystem)

    def reproduce(self, ecosystem):
        if len(ecosystem.herbivores) < 100:  # Limite popolazione
            offspring = Herbivore(
                self.x + random.uniform(-20, 20),
                self.y + random.uniform(-20, 20)
            )
            offspring.energy = 60
            ecosystem.herbivores.append(offspring)
            self.energy -= 40

class Predator(Animal):
    """Predatore - caccia erbivori"""
    def __init__(self, x: float, y: float):
        super().__init__(x, y, RED, speed=2.5, vision_range=120)
        self.max_age = 1200
        self.size = 8

    def update(self, ecosystem):
        super().update(ecosystem)

        if not self.alive:
            return

        # 1. Movimento di base/casuale
        self.move()

        # 2. Cerca prede (priorità)
        nearest_prey = self.find_nearest(ecosystem.herbivores, self.vision_range)

        if nearest_prey and nearest_prey.alive:
            dist = self.distance_to(nearest_prey)

            if dist < 15:  # Abbastanza vicino per cacciare
                # Caccia: fermarsi è meno critico per i predatori, ma manteniamo la stessa struttura
                self.energy += 50
                nearest_prey.alive = False
            else:
                # Se il bersaglio è in vista ma lontano, muovi verso di esso
                self.seek_target(nearest_prey)

        # Riproduzione
        if self.energy >= self.reproduction_threshold and random.random() < 0.002:
            self.reproduce(ecosystem) # <--- Rimosso il ":" finale!

# Il metodo reproduce non ha errori ed è corretto:
    def reproduce(self, ecosystem):
            if len(ecosystem.predators) < 50:  # Limite popolazione
                offspring = Predator(
                self.x + random.uniform(-20, 20),
                self.y + random.uniform(-20, 20)
            )
            offspring.energy = 60
            ecosystem.predators.append(offspring)
            self.energy -= 50
class Ecosystem:
    """Gestisce l'intero ecosistema"""
    def __init__(self):
        self.plants: List[Plant] = []
        self.herbivores: List[Herbivore] = []
        self.predators: List[Predator] = []
        self.stats = Stats()
        self.generation = 0

        # Popolazione iniziale
        self.spawn_initial_population()

    def spawn_initial_population(self):
        # Piante
        for _ in range(5000):
            x = random.randint(50, WIDTH - 50)
            y = random.randint(50, HEIGHT - 50)
            self.plants.append(Plant(x, y))

        # Erbivori
        for _ in range(60):
            x = random.randint(50, WIDTH - 50)
            y = random.randint(50, HEIGHT - 50)
            self.herbivores.append(Herbivore(x, y))

        # Predatori
        for _ in range(3):
            x = random.randint(50, WIDTH - 50)
            y = random.randint(50, HEIGHT - 50)
            self.predators.append(Predator(x, y))

    def update(self):
        # Aggiorna tutte le entità
        for plant in self.plants:
            plant.update(self)

        for herbivore in self.herbivores:
            herbivore.update(self)

        for predator in self.predators:
            predator.update(self)

        # Rimuovi entità morte
        self.plants = [p for p in self.plants if p.alive]
        self.herbivores = [h for h in self.herbivores if h.alive]
        self.predators = [p for p in self.predators if p.alive]

        # Aggiorna statistiche
        self.stats.plants = len(self.plants)
        self.stats.herbivores = len(self.herbivores)
        self.stats.predators = len(self.predators)
        self.generation += 1

    def draw(self, screen):
        for plant in self.plants:
            plant.draw(screen)

        for herbivore in self.herbivores:
            herbivore.draw(screen)

        for predator in self.predators:
            predator.draw(screen)

class Simulation:
    """Gestisce la simulazione e l'interfaccia"""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Simulazione Ecosistema")
        self.clock = pygame.time.Clock()
        self.ecosystem = Ecosystem()
        self.running = True
        self.paused = False
        self.font = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 20)

    def draw_ui(self):
        """Disegna interfaccia utente con statistiche"""
        # Pannello statistiche
        panel_height = 120
        pygame.draw.rect(self.screen, (240, 240, 240), (0, 0, WIDTH, panel_height))
        pygame.draw.line(self.screen, BLACK, (0, panel_height), (WIDTH, panel_height), 2)

        stats = self.ecosystem.stats

        # Testo statistiche
        y_offset = 10
        texts = [
            f"Generazione: {self.generation_display()}",
            f"🌱 Piante: {stats.plants}",
            f"🐰 Erbivori: {stats.herbivores}",
            f"🦁 Predatori: {stats.predators}",
            f"{'⏸ PAUSA' if self.paused else '▶ In esecuzione'} | SPAZIO: pausa | R: reset | +/-: velocità"
        ]

        for i, text in enumerate(texts):
            color = BLACK if i < 4 else BLUE
            font = self.font if i < 4 else self.font_small
            surface = font.render(text, True, color)
            self.screen.blit(surface, (10, y_offset + i * 25))

    def generation_display(self):
        """Formatta il numero di generazione"""
        gen = self.ecosystem.generation
        if gen > 1000:
            return f"{gen//1000}k"
        return str(gen)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused

                elif event.key == pygame.K_r:
                    self.ecosystem = Ecosystem()

                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    global FPS
                    FPS = min(120, FPS + 10)

                elif event.key == pygame.K_MINUS:
                    FPS = max(10, FPS - 10)

            # Click per aggiungere entità
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if y > 120:  # Sotto il pannello UI
                    if event.button == 1:  # Click sinistro - pianta
                        self.ecosystem.plants.append(Plant(x, y))
                    elif event.button == 3:  # Click destro - erbivoro
                        self.ecosystem.herbivores.append(Herbivore(x, y))

    def run(self):
        while self.running:
            self.handle_events()

            if not self.paused:
                self.ecosystem.update()

            # Rendering
            self.screen.fill(LIGHT_GREEN)

            # Disegna ecosistema (con offset per UI)
            temp_surface = pygame.Surface((WIDTH, HEIGHT - 120))
            temp_surface.fill(LIGHT_GREEN)

            # Sposta il contesto di disegno
            for entity in (self.ecosystem.plants + self.ecosystem.herbivores +
                          self.ecosystem.predators):
                old_y = entity.y
                entity.y -= 120
                entity.draw(temp_surface)
                entity.y = old_y

            self.screen.blit(temp_surface, (0, 120))

            self.draw_ui()
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    sim = Simulation()
    sim.run()