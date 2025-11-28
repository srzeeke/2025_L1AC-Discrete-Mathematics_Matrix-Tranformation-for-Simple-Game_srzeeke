import pygame
import sys
import math
import numpy as np

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Matrix Transformation Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

# Font
font = pygame.font.SysFont('Arial', 20)

class Shape:
    def __init__(self, vertices):
        self.original_vertices = np.array(vertices)
        self.vertices = np.array(vertices)
        self.color = BLUE
        self.transform_matrix = np.identity(3)
        
    def apply_transformation(self, matrix):
        # Apply transformation to the shape
        self.transform_matrix = matrix @ self.transform_matrix
        
        # Apply the transformation to each vertex
        transformed_vertices = []
        for vertex in self.original_vertices:
            # Convert to homogeneous coordinates
            homogenous_vertex = np.array([vertex[0], vertex[1], 1])
            
            # Apply transformation
            transformed_vertex = self.transform_matrix @ homogenous_vertex
            
            # Convert back to Cartesian coordinates
            transformed_vertices.append([transformed_vertex[0], transformed_vertex[1]])
        
        self.vertices = np.array(transformed_vertices)
    
    def draw(self, surface):
        # Draw the shape
        if len(self.vertices) > 2:
            pygame.draw.polygon(surface, self.color, self.vertices, 2)
        
        # Draw vertices
        for vertex in self.vertices:
            pygame.draw.circle(surface, RED, (int(vertex[0]), int(vertex[1])), 5)

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        
    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

def create_translation_matrix(tx, ty):
    return np.array([
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ])

def create_rotation_matrix(angle):
    rad = math.radians(angle)
    return np.array([
        [math.cos(rad), -math.sin(rad), 0],
        [math.sin(rad), math.cos(rad), 0],
        [0, 0, 1]
    ])

def create_scaling_matrix(sx, sy):
    return np.array([
        [sx, 0, 0],
        [0, sy, 0],
        [0, 0, 1]
    ])

def main():
    clock = pygame.time.Clock()
    
    # Create a triangle shape
    triangle = Shape([
        [WIDTH // 2, HEIGHT // 2 - 50],
        [WIDTH // 2 - 50, HEIGHT // 2 + 50],
        [WIDTH // 2 + 50, HEIGHT // 2 + 50]
    ])
    
    # Create buttons
    buttons = [
        Button(50, 50, 120, 40, "Translate +X", GRAY, GREEN),
        Button(50, 100, 120, 40, "Translate -X", GRAY, GREEN),
        Button(50, 150, 120, 40, "Translate +Y", GRAY, GREEN),
        Button(50, 200, 120, 40, "Translate -Y", GRAY, GREEN),
        Button(50, 250, 120, 40, "Rotate +30°", GRAY, GREEN),
        Button(50, 300, 120, 40, "Rotate -30°", GRAY, GREEN),
        Button(50, 350, 120, 40, "Scale +10%", GRAY, GREEN),
        Button(50, 400, 120, 40, "Scale -10%", GRAY, GREEN),
        Button(50, 450, 120, 40, "Reset", GRAY, RED)
    ]
    
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Check button clicks
            for i, button in enumerate(buttons):
                button.check_hover(mouse_pos)
                if button.is_clicked(mouse_pos, event):
                    if i == 0:  # Translate +X
                        triangle.apply_transformation(create_translation_matrix(50, 0))
                    elif i == 1:  # Translate -X
                        triangle.apply_transformation(create_translation_matrix(-50, 0))
                    elif i == 2:  # Translate +Y
                        triangle.apply_transformation(create_translation_matrix(0, 50))
                    elif i == 3:  # Translate -Y
                        triangle.apply_transformation(create_translation_matrix(0, -50))
                    elif i == 4:  # Rotate +30°
                        triangle.apply_transformation(create_rotation_matrix(30))
                    elif i == 5:  # Rotate -30°
                        triangle.apply_transformation(create_rotation_matrix(-30))
                    elif i == 6:  # Scale +10%
                        triangle.apply_transformation(create_scaling_matrix(1.1, 1.1))
                    elif i == 7:  # Scale -10%
                        triangle.apply_transformation(create_scaling_matrix(0.9, 0.9))
                    elif i == 8:  # Reset
                        triangle.transform_matrix = np.identity(3)
                        triangle.vertices = triangle.original_vertices.copy()
        
        # Draw everything
        screen.fill(WHITE)
        
        # Draw coordinate system
        pygame.draw.line(screen, BLACK, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 1)
        pygame.draw.line(screen, BLACK, (0, HEIGHT // 2), (WIDTH, HEIGHT // 2), 1)
        
        # Draw shape
        triangle.draw(screen)
        
        # Draw buttons
        for button in buttons:
            button.draw(screen)
        
        # Draw transformation matrix
        matrix_text = "Transformation Matrix:"
        matrix_surface = font.render(matrix_text, True, BLACK)
        screen.blit(matrix_surface, (WIDTH - 300, 50))
        
        for i, row in enumerate(triangle.transform_matrix):
            row_text = f"[{row[0]:.2f}, {row[1]:.2f}, {row[2]:.2f}]"
            row_surface = font.render(row_text, True, BLACK)
            screen.blit(row_surface, (WIDTH - 300, 80 + i * 30))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()