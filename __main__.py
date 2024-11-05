import pygame
import random
import math
import pygame.mixer
import os

# Initialize Pygame
pygame.init()
pygame.mixer.init()

#Audio folder path
Game_audio=os.path.join("seige_spheres","Game_audio")

#Game sounds
paddle_collision=pygame.mixer.Sound(os.path.join(Game_audio,"collision_sound.wav"))
game_music=pygame.mixer.Sound(os.path.join(Game_audio,"game_music.mp3"))
goal_sound=pygame.mixer.Sound(os.path.join(Game_audio,"goal_sound.mp3"))
powerup_sound=pygame.mixer.Sound(os.path.join(Game_audio,"powerup_sound.mp3"))

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PADDLE_RADIUS = 32
BALL_RADIUS = 15
WALL_THICKNESS = 8
CHARACTER_SIZE = 30
FPS = 60
INITIAL_BALL_SPEED = 7
RESPAWN_DELAY = 1000
GOAL_WIDTH = 120
PARTICLE_LIFETIME = 30
PARTICLE_COUNT = 15
GOAL_ANIMATION_DURATION = 60
POWERUP_SIZE = 20
POWERUP_DURATION = 5000
POWERUP_SPAWN_INTERVAL = 10000
POWERUP_SPAWN_CHANCE = 0.7
glow_radius=30,
corner_radius=40

# Colors with alpha for glow effects
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)
ORANGE = (255, 165, 0)
DARK_GREEN = (0, 128, 0)
DARK_RED = (128, 0, 0)


# Ball Class
class Ball:
    def __init__(self, x: float, y: float, radius: float, dx: float, dy: float):
        self.x = x
        self.y = y
        self.radius = radius
        self.dx = dx
        self.dy = dy
        self.active = True
        self.speed = INITIAL_BALL_SPEED
        self.last_collision_time = 0
        self.collision_cooldown = 100

        self.glow_radius = radius * 2
        self.glow_surface = pygame.Surface((self.glow_radius * 2, self.glow_radius * 2), pygame.SRCALPHA)
        self.base_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.base_surface, WHITE, (radius, radius), radius)
        for i in range(10):
            alpha = 100 - i * 10
            size = self.radius + i * 2
            pygame.draw.circle(self.glow_surface, (*WHITE, alpha),
                             (self.glow_radius, self.glow_radius), size)

    def update(self):
        if not self.active:
            return

        next_x = self.x + self.dx * self.speed
        next_y = self.y + self.dy * self.speed

        # Check for collisions with walls (excluding goal areas)
        goal_top = WINDOW_HEIGHT//2 - GOAL_WIDTH//2
        goal_bottom = WINDOW_HEIGHT//2 + GOAL_WIDTH//2

        # Add small buffer to prevent sticking
        buffer = 2

        # Top wall collision
        if next_y - self.radius <= 0:
            self.dy = abs(self.dy)  # Force downward movement
            self.y = self.radius + buffer
            return

        # Bottom wall collision
        if next_y + self.radius >= WINDOW_HEIGHT:
            self.dy = -abs(self.dy)  # Force upward movement
            self.y = WINDOW_HEIGHT - self.radius - buffer
            return

        # Left wall collision (excluding goal)
        if next_x - self.radius <= WALL_THICKNESS:
            if self.y < goal_top or self.y > goal_bottom:
                self.dx = abs(self.dx)  # Force rightward movement
                self.x = WALL_THICKNESS + self.radius + buffer
                return

        # Right wall collision (excluding goal)
        if next_x + self.radius >= WINDOW_WIDTH - WALL_THICKNESS:
            if self.y < goal_top or self.y > goal_bottom:
                self.dx = -abs(self.dx)  # Force leftward movement
                self.x = WINDOW_WIDTH - WALL_THICKNESS - self.radius - buffer
                return

        # If no collisions, update position
        self.x = next_x
        self.y = next_y

    def draw(self, screen):
        # Draw glow
        screen.blit(self.glow_surface,
                   (self.x - self.glow_radius, self.y - self.glow_radius))
        # Draw base ball
        screen.blit(self.base_surface,
                   (self.x - self.radius, self.y - self.radius))

class Player:
    def __init__(self, x: int, side: str):
        self.x = x
        self.y = WINDOW_HEIGHT // 2
        self.radius = PADDLE_RADIUS
        self.score = 0
        self.side = side
        self.speed = 5
        self.color = GREEN if side == 'left' else RED
        self.active_powerups = {}
        self.original_speed = self.speed
        self.original_radius = self.radius

        # Create surfaces for glow effect
        self.glow_radius = PADDLE_RADIUS * 2
        self.glow_surface = pygame.Surface((self.glow_radius * 2, self.glow_radius * 2), pygame.SRCALPHA)
        self.base_surface = pygame.Surface((PADDLE_RADIUS * 2, PADDLE_RADIUS * 2), pygame.SRCALPHA)

        # Color scheme based on side
        self.color_scheme = (GREEN, DARK_GREEN, GREEN) if side == 'left' else (RED, DARK_RED, RED)
        
        # Create a surface for the paddle with transparency
        self.paddle_surface = pygame.Surface((PADDLE_RADIUS * 2, PADDLE_RADIUS * 2), pygame.SRCALPHA)

        # Draw outer layer
        outer_color, main_color, inner_color = self.color_scheme
        pygame.draw.circle(self.paddle_surface, outer_color, (PADDLE_RADIUS, PADDLE_RADIUS), PADDLE_RADIUS)

        # Draw main layer (inner circle for 3D effect)
        main_radius = int(PADDLE_RADIUS * 0.8)
        pygame.draw.circle(self.paddle_surface, main_color, (PADDLE_RADIUS, PADDLE_RADIUS), main_radius)

        # Draw highlight for 3D effect
        highlight_radius = int(PADDLE_RADIUS * 0.5)
        highlight_offset_y = int(PADDLE_RADIUS * 0.05)
        pygame.draw.circle(self.paddle_surface, inner_color, (PADDLE_RADIUS, PADDLE_RADIUS - highlight_offset_y), highlight_radius)

        
        # Create glow effect
        for i in range(10):
            alpha = 100 - i * 10
            size = self.radius + i * 2
            pygame.draw.circle(self.glow_surface, (*self.color, alpha),
                             (self.glow_radius, self.glow_radius), size)


    def move(self, up: bool, left: bool = None):
        # Store previous position for boundary checking
        prev_y = self.y
        prev_x = self.x

        # Vertical movement
        if up is not None:
            if up:
                self.y -= self.speed
            else:
                self.y += self.speed

        # Enforce vertical boundaries with padding
        padding = self.radius + 2  # Add small padding to prevent sticking
        if self.y < padding:
            self.y = padding
        elif self.y > WINDOW_HEIGHT - padding:
            self.y = WINDOW_HEIGHT - padding

        # Horizontal movement with side restrictions
        if left is not None:
            if self.side == 'left':
                if left:
                    self.x -= self.speed
                else:
                    self.x += self.speed

                # Left side boundaries
                if self.x < padding:
                    self.x = padding
                elif self.x > WINDOW_WIDTH//2 - padding:
                    self.x = WINDOW_WIDTH//2 - padding
            else:
                if left:
                    self.x -= self.speed
                else:
                    self.x += self.speed

                # Right side boundaries
                if self.x < WINDOW_WIDTH//2 + padding:
                    self.x = WINDOW_WIDTH//2 + padding
                elif self.x > WINDOW_WIDTH - padding:
                    self.x = WINDOW_WIDTH - padding

    def draw(self, screen):
        # Draw paddle with glow effect
        screen.blit(self.glow_surface,
                   (self.x - self.glow_radius, self.y - self.glow_radius))
        screen.blit(self.base_surface,
                   (self.x - self.radius, self.y - self.radius))
        
        screen.blit(self.paddle_surface, (self.x - PADDLE_RADIUS, self.y - PADDLE_RADIUS))

        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(str(self.score), True, WHITE)
        score_x = 50 if self.side == 'left' else WINDOW_WIDTH - 70
        screen.blit(score_text, (score_x, 30))



    def apply_powerup(self, powerup_type):
        current_time = pygame.time.get_ticks()

        if powerup_type == 'speed_boost':
            self.speed = self.original_speed * 1.5
            self.active_powerups['speed_boost'] = current_time + POWERUP_DURATION

        elif powerup_type == 'size_change':
            self.radius = self.original_radius * 1.5
            # Recreate surfaces with new size
            self.glow_radius = self.radius * 2
            self.glow_surface = pygame.Surface((self.glow_radius * 2, self.glow_radius * 2), pygame.SRCALPHA)
            self.base_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(self.base_surface, self.color, (self.radius, self.radius), self.radius)
            for i in range(10):
                alpha = 100 - i * 10
                size = self.radius + i * 2
                pygame.draw.circle(self.glow_surface, (*self.color, alpha),
                                 (self.glow_radius, self.glow_radius), size)
            self.active_powerups['size_change'] = current_time + POWERUP_DURATION

    def update_powerups(self):
        current_time = pygame.time.get_ticks()
        expired_powerups = []

        for powerup_type, end_time in self.active_powerups.items():
            if current_time >= end_time:
                expired_powerups.append(powerup_type)

        for powerup_type in expired_powerups:
            if powerup_type == 'speed_boost':
                self.speed = self.original_speed
            elif powerup_type == 'size_change':
                self.radius = self.original_radius
                # Recreate surfaces with original size
                self.glow_radius = self.radius * 2
                self.glow_surface = pygame.Surface((self.glow_radius * 2, self.glow_radius * 2), pygame.SRCALPHA)
                self.base_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(self.base_surface, self.color, (self.radius, self.radius), self.radius)
                for i in range(10):
                    alpha = 100 - i * 10
                    size = self.radius + i * 2
                    pygame.draw.circle(self.glow_surface, (*self.color, alpha),
                                     (self.glow_radius, self.glow_radius), size)

            del self.active_powerups[powerup_type]

class PowerUp:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.radius = POWERUP_SIZE
        self.type = random.choice([
            'speed_boost',
            'size_change',
            'ball_speed',
            'multi_ball'
        ])

        # Set color based on power-up type
        self.color = {
            'speed_boost': BLUE,
            'size_change': PURPLE,
            'ball_speed': ORANGE,
            'multi_ball': GREEN
        }[self.type]

        # Create surfaces for glow effect
        self.glow_radius = self.radius * 2
        self.glow_surface = pygame.Surface((self.glow_radius * 2, self.glow_radius * 2), pygame.SRCALPHA)
        self.base_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)

        # Draw the base power-up
        pygame.draw.circle(self.base_surface, self.color, (self.radius, self.radius), self.radius)

        # Create glow effect
        for i in range(10):
            alpha = 100 - i * 10
            size = self.radius + i * 2
            pygame.draw.circle(self.glow_surface, (*self.color, alpha),
                             (self.glow_radius, self.glow_radius), size)

    def draw(self, screen):
        screen.blit(self.glow_surface,
                   (self.x - self.glow_radius, self.y - self.glow_radius))
        screen.blit(self.base_surface,
                   (self.x - self.radius, self.y - self.radius))

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 8)
        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed
        self.lifetime = PARTICLE_LIFETIME
        self.size = random.randint(2, 4)

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.lifetime -= 1
        self.size = max(0, self.size - 0.1)

    def draw(self, screen):
        alpha = int((self.lifetime / PARTICLE_LIFETIME) * 255)
        particle_color = (*self.color[:3], alpha)
        particle_surface = pygame.Surface((int(self.size * 2), int(self.size * 2)), pygame.SRCALPHA)
        pygame.draw.circle(particle_surface, particle_color,
                         (int(self.size), int(self.size)), int(self.size))
        screen.blit(particle_surface, (int(self.x - self.size), int(self.y - self.size)))

class GoalAnimation:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.lifetime = GOAL_ANIMATION_DURATION
        self.scale = 0
        self.max_scale = 2.0
        self.alpha = 255
        self.font = pygame.font.Font(None, 120)

    def update(self):
        self.lifetime -= 1
        progress = 1 - (self.lifetime / GOAL_ANIMATION_DURATION)

        if progress < 0.3:
            self.scale = (progress / 0.3) * self.max_scale
        else:
            self.alpha = int(255 * (1 - ((progress - 0.3) / 0.7)))

    def draw(self, screen):
        text = self.font.render("GOAL!", True, WHITE)
        text_rect = text.get_rect()

        # Create a surface for the scaled text
        scaled_width = int(text_rect.width * self.scale)
        scaled_height = int(text_rect.height * self.scale)
        if scaled_width <= 0 or scaled_height <= 0:
            return

        scaled_surface = pygame.transform.scale(text, (scaled_width, scaled_height))

        # Create a surface with alpha for fading
        alpha_surface = pygame.Surface((scaled_width, scaled_height), pygame.SRCALPHA)
        alpha_surface.fill((255, 255, 255, self.alpha))
        scaled_surface.blit(alpha_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        # Center the text
        dest_rect = scaled_surface.get_rect(center=(self.x, self.y))
        screen.blit(scaled_surface, dest_rect)

class Game:
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Glow Hockey")
        self.clock = pygame.time.Clock()
        game_music.play()

        # Create surfaces for boundary glow effects
        self.boundary_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        self.create_boundary_glow()

        self.player1 = Player(150, 'left')
        self.player2 = Player(WINDOW_WIDTH - 150, 'right')

        self.balls = []
        ranum = random.randrange(2)
        self.spawn_ball('left' if ranum == 0 else 'right')

        self.respawn_timer = 0
        self.should_respawn = False
        self.respawn_side = 'left'
        self.font = pygame.font.Font(None, 36)

        # Lists for particles and animations
        self.particles = []
        self.goal_animations = []
        self.powerups = []
        self.last_powerup_spawn = pygame.time.get_ticks()

    def create_collision_particles(self, x, y, color):
        for _ in range(PARTICLE_COUNT):
            self.particles.append(Particle(x, y, color))


    def create_boundary_glow(self):
        # Top boundary
        for i in range(5):
            alpha = 150 - i * 30
            pygame.draw.rect(self.boundary_surface, (*GREEN, alpha),
                           (0, i, WINDOW_WIDTH, WALL_THICKNESS))

        # Bottom boundary
        for i in range(5):
            alpha = 150 - i * 30
            pygame.draw.rect(self.boundary_surface, (*RED, alpha),
                           (0, WINDOW_HEIGHT - WALL_THICKNESS - i, WINDOW_WIDTH, WALL_THICKNESS))

        # Left boundary (excluding goal area)
        goal_top = WINDOW_HEIGHT//2 - GOAL_WIDTH//2
        goal_bottom = WINDOW_HEIGHT//2 + GOAL_WIDTH//2
        for i in range(5):
            alpha = 150 - i * 30
            pygame.draw.rect(self.boundary_surface, (*GREEN, alpha),
                           (i, 0, WALL_THICKNESS, goal_top))
            pygame.draw.rect(self.boundary_surface, (*GREEN, alpha),
                           (i, goal_bottom, WALL_THICKNESS, WINDOW_HEIGHT - goal_bottom))

        # Right boundary (excluding goal area)
        for i in range(5):
            alpha = 150 - i * 30
            pygame.draw.rect(self.boundary_surface, (*RED, alpha),
                           (WINDOW_WIDTH - WALL_THICKNESS - i, 0, WALL_THICKNESS, goal_top))
            pygame.draw.rect(self.boundary_surface, (*RED, alpha),
                           (WINDOW_WIDTH - WALL_THICKNESS - i, goal_bottom, WALL_THICKNESS, WINDOW_HEIGHT - goal_bottom))

    def spawn_ball(self, side: str):
        x = WINDOW_WIDTH // 4 if side == 'left' else 3 * WINDOW_WIDTH // 4
        y = WINDOW_HEIGHT // 2
        angle = random.uniform(-math.pi/4, math.pi/4)
        if side == 'right':
            angle += math.pi
        dx = math.cos(angle)
        dy = math.sin(angle)
        self.balls.append(Ball(x, y, BALL_RADIUS, dx, dy))

    def check_collision(self, ball, player):
        current_time = pygame.time.get_ticks()
        

        # Check collision cooldown
        if current_time - ball.last_collision_time < ball.collision_cooldown:
            return False

        dx = ball.x - player.x
        dy = ball.y - player.y
        distance = math.sqrt(dx * dx + dy * dy)

        if distance < ball.radius + player.radius:
            paddle_collision.play()

            # Create particles at collision point
            collision_x = player.x + (dx * player.radius / distance)
            collision_y = player.y + (dy * player.radius / distance)
            self.create_collision_particles(collision_x, collision_y, player.color)

            # Calculate new velocity based on collision angle
            angle = math.atan2(dy, dx)

            # Add some randomness to prevent predictable bounces
            angle_variation = random.uniform(-0.1, 0.1)
            angle += angle_variation

            # Ensure minimum angle from horizontal to prevent "flat" bounces
            min_angle = 0.2  # About 11.5 degrees
            if abs(math.sin(angle)) < math.sin(min_angle):
                angle = min_angle if angle > 0 else -min_angle

            # Calculate new velocity
            ball.dx = math.cos(angle)
            ball.dy = math.sin(angle)

            # Normalize velocity vector
            velocity_length = math.sqrt(ball.dx * ball.dx + ball.dy * ball.dy)
            if velocity_length > 0:
                ball.dx /= velocity_length
                ball.dy /= velocity_length

            # Move ball outside of paddle to prevent multiple collisions
            separation_distance = ball.radius + player.radius + 2  # Add small buffer
            ball.x = player.x + math.cos(angle) * separation_distance
            ball.y = player.y + math.sin(angle) * separation_distance

            # Update collision timestamp
            ball.last_collision_time = current_time

            # Increase ball speed slightly after each hit, with a maximum limit
            ball.speed = min(ball.speed * 1.1, 15)
            return True
        return False

    def spawn_powerup(self):
        # Spawn power-up in a random location, avoiding walls and goals
        x = random.randint(WALL_THICKNESS + POWERUP_SIZE,
                          WINDOW_WIDTH - WALL_THICKNESS - POWERUP_SIZE)
        y = random.randint(WALL_THICKNESS + POWERUP_SIZE,
                          WINDOW_HEIGHT - WALL_THICKNESS - POWERUP_SIZE)

        # Avoid spawning in goal areas
        goal_top = WINDOW_HEIGHT//2 - GOAL_WIDTH//2
        goal_bottom = WINDOW_HEIGHT//2 + GOAL_WIDTH//2

        if (x < WALL_THICKNESS * 2 or x > WINDOW_WIDTH - WALL_THICKNESS * 2) and \
           (y > goal_top - POWERUP_SIZE and y < goal_bottom + POWERUP_SIZE):
            return self.spawn_powerup()

        self.powerups.append(PowerUp(x, y))

    def check_powerup_collisions(self):
        for powerup in self.powerups[:]:
            # Check collision with players
            for player in [self.player1, self.player2]:
                dx = powerup.x - player.x
                dy = powerup.y - player.y
                distance = math.sqrt(dx * dx + dy * dy)

                if distance < player.radius + powerup.radius:
                    powerup_sound.play()
                    if powerup.type == 'multi_ball':
                        self.spawn_ball(player.side)
                    elif powerup.type == 'ball_speed':
                        for ball in self.balls:
                            ball.speed *= 1.2
                    else:
                        player.apply_powerup(powerup.type)

                    self.powerups.remove(powerup)
                    self.create_collision_particles(powerup.x, powerup.y, powerup.color)
                    break


    def update(self):

        # Update power-ups
        current_time = pygame.time.get_ticks()
        if current_time - self.last_powerup_spawn >= POWERUP_SPAWN_INTERVAL:
            if random.random() < POWERUP_SPAWN_CHANCE:
                self.spawn_powerup()
            self.last_powerup_spawn = current_time

        self.check_powerup_collisions()
        self.player1.update_powerups()
        self.player2.update_powerups()

        # Update particles
        self.particles = [p for p in self.particles if p.lifetime > 0]
        for particle in self.particles:
            particle.update()

        # Update goal animations
        self.goal_animations = [a for a in self.goal_animations if a.lifetime > 0]
        for animation in self.goal_animations:
            animation.update()

        if self.should_respawn:
            current_time = pygame.time.get_ticks()
            if current_time - self.respawn_timer >= RESPAWN_DELAY:
                self.spawn_ball(self.respawn_side)
                self.should_respawn = False

        for ball in self.balls[:]:
            if not ball.active:
                continue

            # Store previous position
            prev_x = ball.x
            prev_y = ball.y

            ball.update()

            # Check for collisions with paddles
            collision_occurred = False
            for player in [self.player1, self.player2]:
                if self.check_collision(ball, player):
                    collision_occurred = True
                    break

            # If no collision occurred, check if ball is stuck
            if not collision_occurred:
                # If ball hasn't moved much in the last update, give it a small random impulse
                if (abs(ball.x - prev_x) < 0.1 and abs(ball.y - prev_y) < 0.1):
                    ball.dx += random.uniform(-0.1, 0.1)
                    ball.dy += random.uniform(-0.1, 0.1)
                    # Renormalize direction vector
                    magnitude = math.sqrt(ball.dx * ball.dx + ball.dy * ball.dy)
                    if magnitude > 0:
                        ball.dx /= magnitude
                        ball.dy /= magnitude

            # Check for goals
            goal_top = WINDOW_HEIGHT//2 - GOAL_WIDTH//2
            goal_bottom = WINDOW_HEIGHT//2 + GOAL_WIDTH//2

            # Left goal
            if ball.x - ball.radius <= 0 and goal_top <= ball.y <= goal_bottom:
                self.player2.score += 1
                ball.active = False
                self.balls.remove(ball)
                self.respawn_timer = pygame.time.get_ticks()
                self.should_respawn = True
                self.respawn_side = 'left'
                self.goal_animations.append(GoalAnimation(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
                goal_sound.play()

            # Right goal
            elif ball.x + ball.radius >= WINDOW_WIDTH and goal_top <= ball.y <= goal_bottom:
                self.player1.score += 1
                ball.active = False
                self.balls.remove(ball)
                self.respawn_timer = pygame.time.get_ticks()
                self.should_respawn = True
                self.respawn_side = 'right'
                self.goal_animations.append(GoalAnimation(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
                goal_sound.play()

    def draw(self):
        self.screen.fill(BLACK)
        # Draw power-ups
        for powerup in self.powerups:
            powerup.draw(self.screen)

        # Draw active power-up indicators
        for player in [self.player1, self.player2]:
            y_offset = 60
            for powerup_type in player.active_powerups:
                text = self.font.render(powerup_type.replace('_', ' ').title(), True, WHITE)
                x = 50 if player.side == 'left' else WINDOW_WIDTH - 170
                self.screen.blit(text, (x, y_offset))
                y_offset += 25
        # Draw boundaries with glow
        self.screen.blit(self.boundary_surface, (0, 0))

        # Draw center line
        pygame.draw.line(self.screen, (*WHITE,50), (WINDOW_WIDTH // 2, 0), (WINDOW_WIDTH // 2, WINDOW_HEIGHT), 2)

    # Draw center circle
        pygame.draw.circle(self.screen, (*WHITE,50), (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2), 50, 2)

    # Goal areas - semi-circles for each side
        goal_radius = 100  # Customize the radius as needed for the goal area semi-circles
    
    # Left goal semi-circle
        pygame.draw.arc(self.screen, (*WHITE,50), 
                        (-100, WINDOW_HEIGHT // 2 - goal_radius, goal_radius * 2, goal_radius * 2),
                        4.71, 1.57, 2)  # Arc from bottom to top on left side

    # Right goal semi-circle
        pygame.draw.arc(self.screen, (*WHITE,50), 
                    (WINDOW_WIDTH - goal_radius, WINDOW_HEIGHT // 2 - goal_radius, goal_radius * 2, goal_radius * 2),
                    1.57, 4.71, 2)  # Arc from top to bottom on right side
        # Draw players
        self.player1.draw(self.screen)
        self.player2.draw(self.screen)

        for ball in self.balls:
            if ball.active:
                ball.draw(self.screen)

        # Draw particles
        for particle in self.particles:
            particle.draw(self.screen)

        # Draw goal animations
        for animation in self.goal_animations:
            animation.draw(self.screen)

        if self.should_respawn:
            ready_text = self.font.render("Get Ready!", True, YELLOW)
            text_rect = ready_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            self.screen.blit(ready_text, text_rect)

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()

            # Player 1 controls (WASD)
            # Vertical movement
            up1 = None
            if keys[pygame.K_w]:
                up1 = True
            elif keys[pygame.K_s]:
                up1 = False

            # Horizontal movement
            left1 = None
            if keys[pygame.K_a]:
                left1 = True
            elif keys[pygame.K_d]:
                left1 = False

            self.player1.move(up1, left1)

            # Player 2 controls (Arrow keys)
            # Vertical movement
            up2 = None
            if keys[pygame.K_UP]:
                up2 = True
            elif keys[pygame.K_DOWN]:
                up2 = False

            # Horizontal movement
            left2 = None
            if keys[pygame.K_LEFT]:
                left2 = True
            elif keys[pygame.K_RIGHT]:
                left2 = False

            self.player2.move(up2, left2)

            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
