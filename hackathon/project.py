import pygame
import math
import random
pygame.init()


# ==========================================
# WINDOW & DISPLAY SETUP
# ==========================================
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Financial Education Game")
clock = pygame.time.Clock()


# ==========================================
# FONTS & COLORS DEFINITIONS
# ==========================================
font = pygame.font.Font(None, 24)
base_font = pygame.font.Font(None, 32)
big_font = pygame.font.Font(None, 42)
text_color = (255, 255, 255)
white = (255, 255, 255)
color_active = pygame.Color('lightskyblue3')
color_passive = pygame.Color('gray15')
color = color_passive


# ==========================================
# GAME STATES & TRACKING VARIABLES
# ==========================================
current_question_index = 0
error_message = ""
game_result_message = ""
evaluated = False
popup_img = None


desired_return = 0
invest_amount = 0
balance = "Balance: $10,000"


# Master dictionary defining the 4 stock choices
STOCK_MARKET = {
    "AAPL": {"name": "Apple Inc", "price": 225.00},
    "MSFT": {"name": "Microsoft Corp", "price": 415.00},
    "AMZN": {"name": "Amazon.com Inc", "price": 195.00},
    "DIS": {"name": "Walt Disney Co", "price": 95.00},
}


# Sequential allocation tracking
stock_investments = {"AAPL": 0, "AMZN": 0, "DIS": 0, "MSFT": 0}
stock_keys = ["AAPL", "AMZN", "DIS", "MSFT"]
allocating_index = 0


input_rect = pygame.Rect(300, 400, 200, 40)


# Text prompts sequence
questions = [
    "Hi! This is a financial game to help you understand the importance of investing. You have $10,000. What is your desired percent return? (Enter 1 to 100 using %)",
    "Great choice! How much money out of the $10,000 would you like to invest?"
]


# Coordinates for the 4 visual stock boxes
box_1 = pygame.Rect(150, 120, 220, 180) # Apple
box_2 = pygame.Rect(430, 120, 220, 180) # Amazon
box_3 = pygame.Rect(150, 330, 220, 180) # Disney
box_4 = pygame.Rect(430, 330, 220, 180) # Microsoft
boxes = [box_1, box_2, box_3, box_4]


# ==========================================
# ASSET LOADING & IMAGE SCALING
# ==========================================
try:
    apple_png = pygame.transform.smoothscale(pygame.image.load("apple.png"), (300, 300))
    amazon_png = pygame.transform.smoothscale(pygame.image.load("amazon.png"), (300, 300))
    microsoft_png = pygame.transform.smoothscale(pygame.image.load("microsoft.png"), (300, 300))
    disney_png = pygame.transform.smoothscale(pygame.image.load("disney.png"), (300, 300))
except:
    apple_png, amazon_png, microsoft_png, disney_png = None, None, None, None


# ==========================================
# HELPER FUNCTIONS
# ==========================================
def draw_stock_boxes(surface):
    """Draws the four white background boxes for the stock grid screen."""
    for box in boxes:
        pygame.draw.rect(surface, white, box)


def draw_wrapped_text(surface, text, font, color, center_x, y, max_width):
    """Automatically wraps long text into multiple centered lines."""
    words = text.split(" ")
    lines = []
    current_line = ""
    for word in words:
        test_line = f"{current_line} {word}".strip()
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)
       
    line_height = font.get_linesize()
    for i, line in enumerate(lines):
        line_surface = font.render(line, True, color)
        line_rect = line_surface.get_rect()
        line_rect.centerx = center_x
        line_rect.top = y + i * line_height
        surface.blit(line_surface, line_rect)


user_text = ''
active = True
running = True


# ==========================================
# MAIN GAME LOOP
# ==========================================
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        if event.type == pygame.MOUSEBUTTONDOWN:
            if current_question_index < 2:
                if input_rect.collidepoint(event.pos):
                    active = True
                    color = color_active
                else:
                    active = False
                    color = color_passive
            elif current_question_index == 2:  # Clicking stock boxes on the visual screen
                if popup_img is not None:
                    popup_img = None
                elif box_1.collidepoint(event.pos):
                    popup_img = apple_png
                elif box_2.collidepoint(event.pos):
                    popup_img = amazon_png
                elif box_3.collidepoint(event.pos):
                    popup_img = disney_png
                elif box_4.collidepoint(event.pos):
                    popup_img = microsoft_png


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                cleaned_input = user_text.strip()


                # STEP 1: Capture desired return percentage
                if current_question_index == 0:
                    num_str = cleaned_input.replace("%", "").strip()
                    if num_str.isdigit() and 1 <= int(num_str) <= 100:
                        desired_return = int(num_str)
                        error_message = ""
                        current_question_index += 1
                    else:
                        error_message = "Invalid input! Please enter a percentage between 1% and 100%."


                # STEP 2: Capture total money to invest -> moves to Visual Stock Screen
                elif current_question_index == 1:
                    num_str = cleaned_input.replace("$", "").replace(",", "").strip()
                    if num_str.isdigit() and 1 <= int(num_str) <= 10000:
                        invest_amount = int(num_str)
                        error_message = ""
                        current_question_index += 1
                    else:
                        error_message = "Invalid input! Please enter an amount between 1 and 10000."


                # STEP 3: Visual Stock Screen Press Enter to start allocating
                elif current_question_index == 2:
                    error_message = ""
                    current_question_index += 1


                # STEP 4: Sequential allocation loop for the 4 stocks
                elif current_question_index == 3:
                    num_str = cleaned_input.replace("$", "").replace(",", "").strip()
                    if num_str.isdigit():
                        val = int(num_str)
                        current_ticker = stock_keys[allocating_index]
                       
                        current_spent = sum(stock_investments.values())
                        if current_spent + val <= invest_amount:
                            stock_investments[current_ticker] = val
                            error_message = ""
                            user_text = ""
                            allocating_index += 1
                           
                            # Once all 4 are done, go to final results screen (Index 4)
                            if allocating_index >= len(stock_keys):
                                current_question_index += 1
                        else:
                            error_message = "You cannot invest more than your total investment amount!"
                    else:
                        error_message = "Please enter a valid number."


                user_text = ""
            elif active and current_question_index in [0, 1, 3]:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode
   
    screen.fill((30, 30, 30))
   
    # ==========================================
    # SCREEN RENDERING
    # ==========================================
   
    # Render Questions 0 and 1 (Desired return & Total investment)
    if current_question_index < 2:
        draw_wrapped_text(screen, balance, base_font, text_color, 400, 30, 450)
        draw_wrapped_text(screen, questions[current_question_index], base_font, text_color, 400, 150, 550)
       
        text_surface = font.render(user_text, True, (255, 255, 255))
        input_rect.width = max(200, text_surface.get_width() + 10)
        pygame.draw.rect(screen, color, input_rect, 2)
        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 10))
       
        if error_message:
            draw_wrapped_text(screen, error_message, font, (255, 100, 100), 400, 460, 500)


    # Render Step 2: The Big Visual Stock Grid Screen (First instruction phase)
    elif current_question_index == 2:
        draw_stock_boxes(screen)
        draw_wrapped_text(screen, "APPLE", big_font, (0, 0, 0), 260, 200, 200)
        draw_wrapped_text(screen, "DISNEY", big_font, (0, 0, 0), 255, 400, 200)
        draw_wrapped_text(screen, "MICROSOFT", big_font, (0, 0, 0), 545, 400, 200)
        draw_wrapped_text(screen, "AMAZON", big_font, (0, 0, 0), 545, 200, 200)
       
        draw_wrapped_text(screen, "Explore the market! Click boxes to view logos. Press ENTER to allocate money.", font, (255, 255, 255), 400, 30, 700)


        if popup_img is not None:
            pygame.draw.rect(screen, (255, 255, 255), (200, 100, 400, 400))
            pygame.draw.rect(screen, (0, 0, 0), (200, 100, 400, 400), 3)
            img_rect = popup_img.get_rect(center=(400, 300))
            screen.blit(popup_img, img_rect)


    # Render Step 3: Sequential Input Prompts for Allocating Money
    elif current_question_index == 3:
        current_ticker = stock_keys[allocating_index]
        stock_name = STOCK_MARKET[current_ticker]["name"]
        prompt = f"How much of your ${invest_amount} would you like to put into {stock_name}?"
       
        draw_wrapped_text(screen, prompt, base_font, text_color, 400, 150, 550)
       
        text_surface = font.render(user_text, True, (255, 255, 255))
        input_rect.width = max(200, text_surface.get_width() + 10)
        pygame.draw.rect(screen, color_active, input_rect, 2)
        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 10))


        if error_message:
            draw_wrapped_text(screen, error_message, font, (255, 100, 100), 400, 460, 500)


    # Render Step 4: Final Results & Rules Evaluation Screen
    else:
        if not evaluated:
            evaluated = True
            total_allocated = sum(stock_investments.values())
            uninvested_cash = 10000 - total_allocated
           
            # RULE 1: If they invest all their money -> fail
            if total_allocated >= 10000:
                game_result_message = "FAIL: You went all-in and lost everything to high risk!"
            else:
                final_value = uninvested_cash
               
                # RULE 2: Randomizer for each stock market pass or fail
                for ticker, amt in stock_investments.items():
                    if amt > 0:
                        market_passed = random.choice([True, False]) # 50/50 chance
                        if market_passed:
                            final_value += amt * 1.5  # Profit multiplier


                # RULE 3: If you lose all the money you invested -> fail
                if total_allocated > 0 and final_value <= uninvested_cash:
                    game_result_message = "FAIL: Your chosen stocks crashed and you lost your investment!"
                # RULE 4: If you gain profit -> win condition
                elif final_value > 10000:
                    profit = round(final_value - 10000, 2)
                    game_result_message = f"WIN! Your portfolio made a profit of ${profit}!"
                else:
                    game_result_message = "GAME OVER: You broke even."


        draw_wrapped_text(screen, game_result_message, big_font, (255, 255, 0), 400, 250, 700)
           
    pygame.display.flip()
    clock.tick(60)


pygame.quit()
