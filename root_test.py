import sys
import pygame

pygame.init()

size = width, height = 1280, 720
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)
input_box = pygame.Rect(width // 2 - 100, height // 2 + 80, 200, 32)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
active = False
text = ''
welcome_message = font.render("Welcome to Blackjack", True, (255, 255, 255))
enter_name_message = small_font.render("Enter your name:", True, (255, 255, 255))
player_name = None
wallet_balance = 100  # Initial wallet balance
bet_amount = 0  # Initial bet amount
running_bet_label = small_font.render(f"Bet: {bet_amount}$", True, (255, 255, 255))

player_positions = {
    "John": (width - 200, height - 100),
    "Ivan": (width // 2, height - 100),
    "Player": (200, height - 100),
    "Dealer": (width // 2, 50),
}

player_circles = {}  # Dictionary to store the circle positions for each player's hand

# Button properties
button_width = 50
button_height = 30
button_margin = 10
button_font = pygame.font.Font(None, 24)
button_color = pygame.Color('lightgray')
button_active_color = pygame.Color('gray')
button_texts = ["5", "10", "20", "Bet", "Clear"]
buttons = []

for i, text in enumerate(button_texts):
    button_x = width // 2 - (len(button_texts) * (button_width + button_margin) // 2) + i * (button_width + button_margin)
    button_y = height - 50
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    button_text = button_font.render(text, True, (0, 0, 0))
    buttons.append((button_rect, button_text, button_color, text))

running = True
first_input = True  # Track if it's the first input

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                active = not active
                if first_input:
                    text = ''
                    first_input = False
            else:
                active = False
            color = color_active if active else color_inactive
            # Check if any button is clicked
            for button_rect, _, _, button_text in buttons:
                if button_rect.collidepoint(event.pos):
                    if button_text == "5":
                        bet_amount += 5
                    elif button_text == "10":
                        bet_amount += 10
                    elif button_text == "20":
                        bet_amount += 20
                    elif button_text == "Clear":
                        bet_amount = 0
                    elif button_text == "Bet":
                        # Perform the final bet action here
                        # This is just a placeholder action
                        print(f"Final bet amount: {bet_amount}$")
        elif event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    player_name = text
                    text = ''
                    active = False
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

    screen.fill((0, 0, 0))
    if player_name is None:
        screen.blit(welcome_message, (width // 2 - welcome_message.get_width() // 2, height // 2 - 100))
        screen.blit(enter_name_message, (width // 2 - enter_name_message.get_width() // 2, height // 2))
        pygame.draw.rect(screen, color, input_box, 2)
        txt_surface = small_font.render(text, True, (255, 255, 255))
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        input_box.w = max(200, txt_surface.get_width() + 10)
    else:
        # Display the players' names in their appropriate positions
        for player, position in player_positions.items():
            if player == "Player":
                player_label = small_font.render(player_name, True, (255, 255, 255))
            else:
                player_label = small_font.render(player, True, (255, 255, 255))
            screen.blit(player_label, (position[0] - player_label.get_width() // 2, position[1]))

            # Calculate the circle position based on the player's position
            if player == "Dealer":
                circle_center_x = position[0]
                circle_center_y = position[1] + player_label.get_height() // 2 + 40
            else:
                circle_center_x = position[0]
                circle_center_y = position[1] - player_label.get_height() // 2 - 30

            # Draw circle for each player's hand
            circle_radius = 30
            pygame.draw.circle(screen, (255, 255, 255), (circle_center_x, circle_center_y), circle_radius, 2)

            # Store the circle position in the dictionary
            player_circles[player] = (circle_center_x, circle_center_y)

        # Display wallet balance in the top-left corner
        wallet_label = small_font.render(f"Wallet: {wallet_balance}$", True, (255, 255, 255))
        screen.blit(wallet_label, (10, 10))

        # Display running bet amount below wallet balance
        screen.blit(running_bet_label, (10, 50))

        # Draw buttons
        for button_rect, button_text, button_color, _ in buttons:
            pygame.draw.rect(screen, button_color, button_rect)
            screen.blit(button_text, button_rect.move(5, 5))

        # Update running bet label text
        running_bet_label = small_font.render(f"Bet: {bet_amount}$", True, (255, 255, 255))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
