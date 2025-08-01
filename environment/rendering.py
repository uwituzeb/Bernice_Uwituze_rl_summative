import pygame
import numpy as np
import math
import random
from typing import List, Dict, Tuple, Optional


class Particle:
    """Particle for visual effects"""
    def __init__(self, x: float, y: float, vx: float, vy: float, 
                 color: Tuple[int, int, int], lifetime: float):
        pygame.font.init()
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = random.uniform(2, 6)
    
    def update(self, dt: float):
        """Update particle physics"""
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += 50 * dt  # Gravity
        self.lifetime -= dt
        self.size *= 0.99  # Shrink over time
    
    def is_dead(self) -> bool:
        return self.lifetime <= 0


class Rendering:
    def __init__(self, window_size: int = 800):
        self.window_size = window_size
        self.cell_size = window_size // 8
        self.particles = []
        
        # Enhanced colors with gradients
        self.colors = {
            'background': (240, 248, 255),  # AliceBlue
            'grid': (200, 200, 200),
            'agent': (65, 105, 225),  # RoyalBlue
            'agent_glow': (135, 206, 250),  # SkyBlue
            'course': (34, 139, 34),  # ForestGreen
            'extracurricular': (0, 191, 255),  # DeepSkyBlue
            'internship': (138, 43, 226),  # BlueViolet
            'distraction': (220, 20, 60),  # Crimson
            'text': (50, 50, 50),
            'ui_bg': (255, 255, 255, 200),
            'progress_bar': (50, 205, 50),  # LimeGreen
            'progress_bg': (220, 220, 220),
            'particle_course': (144, 238, 144),  # LightGreen
            'particle_extracurricular': (173, 216, 230),  # LightBlue
            'particle_internship': (221, 160, 221),  # Plum
            'particle_distraction': (255, 182, 193)  # LightCoral
        }
        
        # Animation properties
        self.animation_speed = 0.1
        self.pulse_animation = 0
        self.float_animation = 0
        self.rotation_animation = 0
        
        # Load fonts
        self.fonts = {}
        self._load_fonts()
        
        # Create enhanced graphics
        self.graphics = self._create_enhanced_graphics()
        
        # Visual effects
        self.screen_shake = 0
        self.flash_effect = 0
        
    def _load_fonts(self):
        """Load pygame fonts for UI elements"""
        try:
            self.fonts['large'] = pygame.font.Font(None, 36)
            self.fonts['medium'] = pygame.font.Font(None, 24)
            self.fonts['small'] = pygame.font.Font(None, 18)
        except:
            self.fonts['large'] = pygame.font.Font(None, 36)
            self.fonts['medium'] = pygame.font.Font(None, 24)
            self.fonts['small'] = pygame.font.Font(None, 18)
    
    def _create_enhanced_graphics(self) -> Dict:
        """Create enhanced graphics with gradients and effects"""
        graphics = {}
        cell_size = self.cell_size
        
        # Course graphic with gradient
        course_surf = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
        # Create gradient effect
        for i in range(cell_size):
            alpha = int(255 * (1 - i / cell_size))
            color = (*self.colors['course'], alpha)
            pygame.draw.line(course_surf, color, (0, i), (cell_size, i))
        # Add book icon
        pygame.draw.rect(course_surf, (255, 255, 255), (cell_size//4, cell_size//4, cell_size//2, cell_size//2))
        pygame.draw.rect(course_surf, self.colors['course'], (cell_size//3, cell_size//3, cell_size//3, cell_size//3))
        graphics['course'] = course_surf
        
        # Extracurricular graphic with star effect
        extracurricular_surf = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
        # Gradient background
        for i in range(cell_size):
            alpha = int(255 * (1 - i / cell_size))
            color = (*self.colors['extracurricular'], alpha)
            pygame.draw.line(extracurricular_surf, color, (0, i), (cell_size, i))
        # Draw star
        center = (cell_size//2, cell_size//2)
        radius = cell_size//3
        points = []
        for i in range(10):
            angle = i * math.pi / 5
            r = radius if i % 2 == 0 else radius * 0.5
            x = center[0] + r * math.cos(angle)
            y = center[1] + r * math.sin(angle)
            points.append((x, y))
        if len(points) > 2:
            pygame.draw.polygon(extracurricular_surf, (255, 255, 255), points)
        graphics['extracurricular'] = extracurricular_surf
        
        # Internship graphic with briefcase
        internship_surf = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
        # Gradient background
        for i in range(cell_size):
            alpha = int(255 * (1 - i / cell_size))
            color = (*self.colors['internship'], alpha)
            pygame.draw.line(internship_surf, color, (0, i), (cell_size, i))
        # Briefcase
        handle_width = cell_size//4
        handle_height = cell_size//6
        case_width = cell_size//2
        case_height = cell_size//2
        pygame.draw.rect(internship_surf, (255, 255, 255), 
                        (cell_size//2 - handle_width//2, cell_size//3, handle_width, handle_height))
        pygame.draw.rect(internship_surf, (255, 255, 255),
                        (cell_size//2 - case_width//2, cell_size//3 + handle_height, case_width, case_height))
        graphics['internship'] = internship_surf
        
        # Distraction graphic with warning effect
        distraction_surf = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
        # Gradient background
        for i in range(cell_size):
            alpha = int(255 * (1 - i / cell_size))
            color = (*self.colors['distraction'], alpha)
            pygame.draw.line(distraction_surf, color, (0, i), (cell_size, i))
        # Phone icon
        phone_width = cell_size//3
        phone_height = cell_size//2
        pygame.draw.rect(distraction_surf, (255, 255, 255),
                        (cell_size//2 - phone_width//2, cell_size//2 - phone_height//2, phone_width, phone_height))
        pygame.draw.rect(distraction_surf, self.colors['distraction'],
                        (cell_size//2 - phone_width//3, cell_size//2 - phone_height//3, phone_width//1.5, phone_height//1.5))
        graphics['distraction'] = distraction_surf
        
        return graphics
    
    def add_particles(self, x: float, y: float, color: Tuple[int, int, int], count: int = 10):
        """Add particle burst effect"""
        for _ in range(count):
            vx = random.uniform(-100, 100)
            vy = random.uniform(-200, -50)
            lifetime = random.uniform(0.5, 1.5)
            self.particles.append(Particle(x, y, vx, vy, color, lifetime))
    
    def update_animations(self, dt: float):
        """Update animation timers and particles"""
        self.pulse_animation += dt * 3
        self.float_animation += dt * 2
        self.rotation_animation += dt * 1.5
        
        # Update particles
        self.particles = [p for p in self.particles if not p.is_dead()]
        for particle in self.particles:
            particle.update(dt)
        
        # Update effects
        self.screen_shake = max(0, self.screen_shake - dt * 5)
        self.flash_effect = max(0, self.flash_effect - dt * 3)
    
    def trigger_screen_shake(self, intensity: float = 10):
        """Trigger screen shake effect"""
        self.screen_shake = intensity
    
    def trigger_flash(self, intensity: float = 1.0):
        """Trigger flash effect"""
        self.flash_effect = intensity
    
    def draw_environment(self, window, agent_location: List[int], 
                       opportunity_cells: List[Dict], distraction_cells: List[Tuple],
                       readiness_score: int, steps_taken: int, max_steps: int) -> pygame.Surface:
        """Draw the enhanced environment with advanced effects"""
        canvas = pygame.Surface((self.window_size, self.window_size), pygame.SRCALPHA)
        canvas.fill(self.colors['background'])
        
        # Apply screen shake
        shake_x = random.uniform(-self.screen_shake, self.screen_shake) if self.screen_shake > 0 else 0
        shake_y = random.uniform(-self.screen_shake, self.screen_shake) if self.screen_shake > 0 else 0
        
        # Draw background pattern with parallax effect
        self._draw_background_pattern(canvas, shake_x * 0.1, shake_y * 0.1)
        
        # Draw grid with subtle animation
        self._draw_grid(canvas, shake_x, shake_y)
        
        # Draw cells with enhanced animations
        self._draw_opportunities(canvas, opportunity_cells, shake_x, shake_y)
        self._draw_distractions(canvas, distraction_cells, shake_x, shake_y)
        
        # Draw agent with advanced effects
        self._draw_agent(canvas, agent_location, shake_x, shake_y)
        
        # Draw particles
        self._draw_particles(canvas)
        
        # Draw UI elements
        self._draw_enhanced_ui(canvas, readiness_score, steps_taken, max_steps)
        
        # Apply flash effect
        if self.flash_effect > 0:
            flash_surf = pygame.Surface((self.window_size, self.window_size), pygame.SRCALPHA)
            flash_surf.fill((255, 255, 255, int(255 * self.flash_effect)))
            canvas.blit(flash_surf, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        
        return canvas
    
    def _draw_background_pattern(self, canvas, offset_x: float = 0, offset_y: float = 0):
        """Draw animated background pattern"""
        for i in range(0, self.window_size, 40):
            for j in range(0, self.window_size, 40):
                x = i + offset_x
                y = j + offset_y
                if (i + j) % 80 == 0:
                    size = 2 + math.sin(self.float_animation + i * 0.01) * 1
                    pygame.draw.circle(canvas, (245, 245, 245), (int(x), int(y)), int(size))
    
    def _draw_grid(self, canvas, shake_x: float = 0, shake_y: float = 0):
        """Draw animated grid lines"""
        grid_size = 8
        for i in range(grid_size + 1):
            pos = i * self.cell_size
            alpha = int(200 + 55 * math.sin(self.pulse_animation + i * 0.5))
            color = (*self.colors['grid'], alpha)
            
            # Create temporary surface for alpha blending
            line_surf = pygame.Surface((self.window_size, 2), pygame.SRCALPHA)
            pygame.draw.line(line_surf, color, (0, 0), (self.window_size, 0), 1)
            canvas.blit(line_surf, (shake_x, pos + shake_y))
            
            line_surf = pygame.Surface((2, self.window_size), pygame.SRCALPHA)
            pygame.draw.line(line_surf, color, (0, 0), (0, self.window_size), 1)
            canvas.blit(line_surf, (pos + shake_x, shake_y))
    
    def _draw_opportunities(self, canvas, opportunity_cells, shake_x: float = 0, shake_y: float = 0):
        """Draw opportunity cells with enhanced animations"""
        for opp in opportunity_cells:
            i, j = opp["pos"]
            x = j * self.cell_size + shake_x
            y = i * self.cell_size + shake_y
            
            # Add floating animation
            float_offset = math.sin(self.float_animation + i + j) * 3
            y += float_offset
            
            # Add rotation effect
            rotation = math.sin(self.rotation_animation + i + j) * 5
            
            # Draw the graphic with rotation
            graphic = self.graphics[opp["type"]]
            rotated_graphic = pygame.transform.rotate(graphic, rotation)
            canvas.blit(rotated_graphic, (x, y))
            
            # Add pulse effect
            pulse_alpha = int(128 + 64 * math.sin(self.pulse_animation + i + j))
            pulse_surf = pygame.Surface((self.cell_size, self.cell_size), pygame.SRCALPHA)
            pulse_surf.fill((255, 255, 255, pulse_alpha))
            canvas.blit(pulse_surf, (x, y), special_flags=pygame.BLEND_RGBA_MULT)
    
    def _draw_distractions(self, canvas, distraction_cells, shake_x: float = 0, shake_y: float = 0):
        """Draw distraction cells with warning effects"""
        for i, j in distraction_cells:
            x = j * self.cell_size + shake_x
            y = i * self.cell_size + shake_y
            
            # Add warning animation
            warning_alpha = int(128 + 64 * math.sin(self.pulse_animation * 2 + i + j))
            warning_surf = pygame.Surface((self.cell_size, self.cell_size), pygame.SRCALPHA)
            warning_surf.fill((255, 0, 0, warning_alpha))
            canvas.blit(warning_surf, (x, y), special_flags=pygame.BLEND_RGBA_MULT)
            
            # Draw the graphic
            graphic = self.graphics['distraction']
            canvas.blit(graphic, (x, y))
    
    def _draw_agent(self, canvas, agent_location, shake_x: float = 0, shake_y: float = 0):
        """Draw the agent with advanced effects"""
        x = agent_location[1] * self.cell_size + self.cell_size // 2 + shake_x
        y = agent_location[0] * self.cell_size + self.cell_size // 2 + shake_y
        
        # Draw multiple glow layers for depth
        for i in range(3):
            glow_radius = int(self.cell_size // 2 + 5 * math.sin(self.pulse_animation) + i * 5)
            glow_alpha = 50 - i * 15
            glow_surf = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (*self.colors['agent_glow'], glow_alpha), 
                             (glow_radius, glow_radius), glow_radius)
            canvas.blit(glow_surf, (x - glow_radius, y - glow_radius))
        
        # Draw main agent circle with gradient
        radius = self.cell_size // 3
        for i in range(radius):
            alpha = int(255 * (1 - i / radius))
            color = (*self.colors['agent'], alpha)
            pygame.draw.circle(canvas, color, (int(x), int(y)), radius - i)
        
        # Draw agent details (eyes with animation)
        eye_offset = self.cell_size // 8
        eye_blink = math.sin(self.pulse_animation * 2) > 0.8
        if not eye_blink:
            pygame.draw.circle(canvas, (255, 255, 255), (int(x - eye_offset), int(y - eye_offset)), 3)
            pygame.draw.circle(canvas, (255, 255, 255), (int(x + eye_offset), int(y - eye_offset)), 3)
            pygame.draw.circle(canvas, (0, 0, 0), (int(x - eye_offset), int(y - eye_offset)), 1)
            pygame.draw.circle(canvas, (0, 0, 0), (int(x + eye_offset), int(y - eye_offset)), 1)
    
    def _draw_particles(self, canvas):
        """Draw particle effects"""
        for particle in self.particles:
            # alpha = int(255 * (particle.lifetime / particle.max_lifetime))
            color = particle.color
            pygame.draw.circle(canvas, color, (int(particle.x), int(particle.y)), int(particle.size))
    
    def _draw_enhanced_ui(self, canvas, readiness_score, steps_taken, max_steps):
        """Draw enhanced UI elements"""
        # Create UI panel with gradient
        ui_height = 120
        ui_surf = pygame.Surface((self.window_size, ui_height), pygame.SRCALPHA)
        
        # Gradient background
        for i in range(ui_height):
            alpha = int(200 * (1 - i / ui_height))
            color = (*self.colors['ui_bg'][:3], alpha)
            pygame.draw.line(ui_surf, color, (0, i), (self.window_size, i))
        
        # Draw readiness score with glow
        score_text = self.fonts['large'].render(f"Readiness Score: {readiness_score}", True, self.colors['text'])
        text_glow = self.fonts['large'].render(f"Readiness Score: {readiness_score}", True, (255, 255, 255))
        ui_surf.blit(text_glow, (22, 22))  # Glow effect
        ui_surf.blit(score_text, (20, 20))
        
        # Draw animated progress bar
        progress_width = self.window_size - 40
        progress_height = 20
        progress_x, progress_y = 20, 60
        
        # Background with gradient
        for i in range(progress_height):
            alpha = int(255 * (1 - i / progress_height))
            color = (*self.colors['progress_bg'], alpha)
            pygame.draw.line(ui_surf, color, (progress_x, progress_y + i), 
                           (progress_x + progress_width, progress_y + i))
        
        # Progress with animation
        progress_ratio = min(1.0, steps_taken / max_steps)
        progress_fill_width = int(progress_width * progress_ratio)
        
        # Animated progress bar
        animation_offset = math.sin(self.pulse_animation) * 2
        for i in range(progress_height):
            alpha = int(255 * (1 - i / progress_height))
            color = (*self.colors['progress_bar'], alpha)
            pygame.draw.line(ui_surf, color, (progress_x, progress_y + i + animation_offset), 
                           (progress_x + progress_fill_width, progress_y + i + animation_offset))
        
        # Progress text
        progress_text = self.fonts['small'].render(f"Progress: {steps_taken}/{max_steps}", True, self.colors['text'])
        ui_surf.blit(progress_text, (progress_x, progress_y + 25))
        
        # Draw animated legend
        legend_y = 90
        legend_items = [
            ("Course", self.colors['course']),
            ("Extracurricular", self.colors['extracurricular']),
            ("Internship", self.colors['internship']),
            ("Distraction", self.colors['distraction'])
        ]
        
        x_offset = 20
        for text, color in legend_items:
            # Animated legend items
            pulse = math.sin(self.pulse_animation + x_offset * 0.1) * 0.2 + 0.8
            size = int(15 * pulse)
            pygame.draw.rect(ui_surf, color, (x_offset, legend_y, size, size))
            legend_text = self.fonts['small'].render(text, True, self.colors['text'])
            ui_surf.blit(legend_text, (x_offset + 20, legend_y))
            x_offset += 150
        
        # Blit UI to canvas
        canvas.blit(ui_surf, (0, self.window_size - ui_height)) 