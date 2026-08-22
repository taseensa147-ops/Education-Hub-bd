import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Display Config
WIDTH, HEIGHT = 430, 750
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Duochingo - Word Match")

# Color Palette (Duolingo Dark Theme)
BG_COLOR = (15, 23, 42)
CARD_DEFAULT = (30, 41, 59)
CARD_BORDER = (51, 65, 85)
CARD_SELECTED = (56, 189, 248)
CARD_MATCHED = (34, 197, 94)
CARD_WRONG = (239, 68, 68)
TEXT_COLOR = (248, 250, 252)

# Load Bengali-compatible System Font
try:
    FONT = pygame.font.SysFont("Kalpurush", 22)
    HEADER_FONT = pygame.font.SysFont("Kalpurush", 26, bold=True)
except:
    FONT = pygame.font.SysFont("Arial", 22)
    HEADER_FONT = pygame.font.SysFont("Arial", 26, bold=True)

# Vocabulary Pairs (Bangla : English)
WORD_PAIRS = {
    "পছন্দ": "like",
    "টেবিল": "table",
    "পরিষ্কার": "clean",
    "বিড়াল": "cat",
    "চাওয়া": "want"
}

class Card:
    def __init__(self, text, x, y, width, height, pair_id):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.pair_id = pair_id  # Unique ID connecting English and Bangla pair
        self.state = "default"  # "default", "selected", "matched", "wrong"

    def draw(self, surface):
        if self.state == "matched":
            return  # Hide matched cards

        color = CARD_DEFAULT
        border_color = CARD_BORDER

        if self.state == "selected":
            color = (14, 116, 144)
            border_color = CARD_SELECTED
        elif self.state == "wrong":
            color = (153, 27, 27)
            border_color = CARD_WRONG

        pygame.draw.rect(surface, color, self.rect, border_radius=12)
        pygame.draw.rect(surface, border_color, self.rect, width=2, border_radius=12)

        text_surf = FONT.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

def setup_game():
    cards = []
    items = []
    
    # Assign pair identifiers
    for idx, (bn, en) in enumerate(WORD_PAIRS.items()):
        items.append((bn, idx))
        items.append((en, idx))
    
    random.shuffle(items)

    # Grid Setup (2 columns, 5 rows)
    col_width = 170
    row_height = 55
    start_x = 30
    start_y = 120
    gap_x = 30
    gap_y = 15

    for i, (text, pair_id) in enumerate(items):
        col = i % 2
        row = i // 2
        x = start_x + col * (col_width + gap_x)
        y = start_y + row * (row_height + gap_y)
        cards.append(Card(text, x, y, col_width, row_height, pair_id))

    return cards

def main():
    clock = pygame.time.Clock()
    cards = setup_game()
    selected_cards = []
    reset_timer = 0

    running = True
    while running:
        SCREEN.fill(BG_COLOR)

        # Header Title
        title_surf = HEADER_FONT.render("জোড়া মেলাতে স্পর্শ করুন", True, TEXT_COLOR)
        SCREEN.blit(title_surf, title_surf.get_rect(center=(WIDTH // 2, 50)))

        # Handle wrong match reset animation timer
        if reset_timer and pygame.time.get_ticks() > reset_timer:
            for card in selected_cards:
                card.state = "default"
            selected_cards = []
            reset_timer = 0

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not reset_timer:
                pos = event.pos
                for card in cards:
                    if card.rect.collidepoint(pos) and card.state == "default":
                        card.state = "selected"
                        selected_cards.append(card)

                        # Two cards selected logic
                        if len(selected_cards) == 2:
                            card1, card2 = selected_cards
                            if card1.pair_id == card2.pair_id:
                                card1.state = "matched"
                                card2.state = "matched"
                                selected_cards = []
                            else:
                                card1.state = "wrong"
                                card2.state = "wrong"
                                reset_timer = pygame.time.get_ticks() + 600  # Pause 600ms to show red mismatch

        # Draw Cards
        for card in cards:
            card.draw(SCREEN)

        # Check win condition
        if all(card.state == "matched" for card in cards):
            win_surf = HEADER_FONT.render("চমৎকার! (Completed)", True, CARD_MATCHED)
            SCREEN.blit(win_surf, win_surf.get_rect(center=(WIDTH // 2, HEIGHT - 100)))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()