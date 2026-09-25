import pygame
import random
from queue import PriorityQueue

WIDTH = 600
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Алгоритм A* — Вариант 20 и Режимы")

# Цветовая гамма из отчета
WHITE = (255, 255, 255)      # Пустая ячейка
BLACK = (0, 0, 0)          # Препятствие
GREY = (128, 128, 128)     # Линии сетки
ORANGE = (255, 165, 0)     # Начало
TURQUOISE = (64, 224, 208) # Конец
GREEN = (0, 255, 0)        # В очереди (open_set)
RED = (255, 0, 0)          # Посещена (closed_set)
PURPLE = (128, 0, 128)     # Путь

# Цвета для отображения весов на взвешенной карте
WEIGHT_COLORS = {
    1: (255, 255, 255),
    2: (220, 245, 220),
    3: (180, 220, 180),
    4: (140, 195, 140),
    5: (100, 160, 100)
}

class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        self.weight = 1  # Вес ячейки по умолчанию

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE
        self.weight = 1

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        # Если ячейка пустая и у нее вес > 1, подкрашиваем ее в зависимости от веса
        if self.color == WHITE and self.weight > 1:
            draw_color = WEIGHT_COLORS.get(self.weight, WHITE)
        else:
            draw_color = self.color

        pygame.draw.rect(win, draw_color, (self.x, self.y, self.width, self.width))

        # Отрисовка текста веса, если он больше 1 и ячейка не барьер/старт/финиш
        if self.weight > 1 and self.color == WHITE and self.width >= 40:
            font = pygame.font.SysFont("comicsans", 14)
            label = font.render(f"w:{self.weight}", 1, (50, 50, 50))
            win.blit(label, (self.x + 3, self.y + 3))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False

def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def a_star_algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            # Учитываем индивидуальный вес ячейки (как в вашем отчете)
            temp_g_score = g_score[current] + neighbor.weight

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win, rows, width)
    pygame.display.update()

def load_variant_20(grid, start, end):
    """Загрузка стен для Варианта №20."""
    for row in grid:
        for spot in row:
            spot.reset()
    walls = [
        (0, 7), (0, 8), (1, 0), (1, 3), (1, 6), (2, 7), (3, 6), (3, 8),
        (4, 0), (4, 9), (5, 0), (6, 5), (6, 7), (7, 4), (7, 6), (7, 7),
        (8, 1), (8, 3), (9, 2), (9, 4), (9, 6)
    ]
    for r, c in walls:
        grid[r][c].make_barrier()

def generate_random_field(grid, start, end):
    """Генерация случайного поля (без весов)."""
    for row in grid:
        for spot in row:
            spot.reset()
            if random.random() < 0.2:  # 20% шанс стены
                spot.make_barrier()

def generate_weighted_map(grid, start, end):
    """Генерация случайной взвешенной карты (Рис. 6)."""
    for row in grid:
        for spot in row:
            spot.reset()
            if random.random() < 0.15:
                spot.make_barrier()
            else:
                spot.weight = random.randint(1, 5)

def main():
    ROWS = 10
    grid = make_grid(ROWS, WIDTH)
    
    start = grid[7][0]
    end = grid[9][9]
    start.make_start()
    end.make_end()
    
    # По умолчанию при старте загружаем Вариант 20
    load_variant_20(grid, start, end)
    
    run = True
    while run:
        draw(WIN, grid, ROWS, WIDTH)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    a_star_algorithm(lambda: draw(WIN, grid, ROWS, WIDTH), grid, start, end)
                
                # Клавиша 1: Вариант 20
                if event.key == pygame.K_1:
                    start = grid[7][0]
                    end = grid[9][9]
                    load_variant_20(grid, start, end)
                    start.make_start()
                    end.make_end()
                    pygame.display.set_caption("Алгоритм A* — Вариант 20")

                # Клавиша 2: Случайное поле (Рис. 4)
                if event.key == pygame.K_2:
                    start = grid[7][0]
                    end = grid[9][9]
                    generate_random_field(grid, start, end)
                    start.make_start()
                    end.make_end()
                    pygame.display.set_caption("Алгоритм A* — Случайное поле")

                # Клавиша 3: Случайная взвешенная карта (Рис. 6)
                if event.key == pygame.K_3:
                    start = grid[7][0]
                    end = grid[9][9]
                    generate_weighted_map(grid, start, end)
                    start.make_start()
                    end.make_end()
                    pygame.display.set_caption("Алгоритм A* — Случайная карта с весами")

                # Клавиша C: Сброс
                if event.key == pygame.K_c:
                    for row in grid:
                        for spot in row:
                            spot.reset()
                    start.make_start()
                    end.make_end()

    pygame.quit()

if __name__ == "__main__":
    main()
