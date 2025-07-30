# ===================================================================================
# SECTION 1: INITIALIZATION AND SETUP
# This section imports necessary libraries, initializes Pygame, and sets up the
# main game window, assets, and fonts.
# ===================================================================================

# ---------------------------------
# 1.1 IMPORTS AND INITIALIZATION
# ---------------------------------
import pygame  # Imports the main Pygame library for game development.
import random  # Imports the random library for generating random numbers (e.g., for alien positions).
import math  # Imports the math library, though it's not used in the final version, it's good practice for game math.
import json  # Imports the JSON library to work with JSON files for saving and loading user data.
import os  # Imports the os library to interact with the operating system, used here to check for file existence.

pygame.init()  # Initializes all the imported Pygame modules required for the game to run.

# ---------------------------------
# 1.2 SCREEN AND DISPLAY SETUP
# ---------------------------------
WIDTH, HEIGHT = 1920, 1080  # Sets the width and height of the game window in pixels.
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Creates the main game window with the specified dimensions.
pygame.display.set_caption("EXODUS")  # Sets the title of the game window.

# Attempt to load and set the window icon, with error handling.
try:
    icon = pygame.image.load('spacecraft.png')  # Loads the icon image from a file.
    pygame.display.set_icon(icon)  # Sets the loaded image as the window's icon.
except pygame.error as e:  # Catches an error if the image file cannot be loaded.
    print(f"Warning: Could not load icon 'spacecraft.png'. Error: {e}")  # Prints a warning message to the console.

# ---------------------------------
# 1.3 ASSET LOADING
# ---------------------------------
# Attempt to load all game images, with error handling to ensure the game can't run without them.
try:
    background = pygame.transform.scale(pygame.image.load('bg3.png'),
                                        (WIDTH, HEIGHT))  # Loads and scales the background image to fit the screen.
    player_img = pygame.transform.scale(pygame.image.load('jet.png'),
                                        (60, 60))  # Loads and scales the player's ship image.
    bullet_img = pygame.transform.scale(pygame.image.load('bullet.png'), (20, 40))  # Loads and scales the bullet image.
    alien_img = pygame.transform.scale(pygame.image.load('alien.png'), (60, 60))  # Loads and scales the alien image.
except pygame.error as e:  # Catches an error if any image file fails to load.
    print(
        f"Fatal Error: Could not load game assets. Please ensure image files are in the correct directory. Error: {e}")  # Prints a fatal error message.
    pygame.quit()  # Quits all Pygame modules.
    exit()  # Exits the Python script.

# ---------------------------------
# 1.4 FONT SETUP
# ---------------------------------
title_font = pygame.font.Font(None,
                              100)  # Creates a font object for large title text. 'None' uses the default Pygame font.
text_font = pygame.font.Font(None, 50)  # Creates a font object for standard text.
small_font = pygame.font.Font(None, 35)  # Creates a font object for smaller informational text.

# ===================================================================================
# SECTION 2: DATA HANDLING AND REUSABLE COMPONENTS
# This section contains functions and classes for handling user data (login/scores)
# and creating reusable UI elements like buttons and input boxes.
# ===================================================================================

# ---------------------------------
# 2.1 USER DATA FILE SETUP
# ---------------------------------
USER_DATA_FILE = 'users.json'  # Defines the constant filename for storing user data.

# Check if the user data file exists, and create it if it doesn't.
if not os.path.exists(USER_DATA_FILE):  # Checks if a file with the given name does not exist in the directory.
    with open(USER_DATA_FILE,
              'w') as f:  # Opens the file in write mode ('w'), which creates it. 'with' ensures it's properly closed.
        json.dump({}, f)  # Writes an empty JSON object ({}) to the new file.


# Function to load user data from the JSON file.
def load_users():
    """Loads a dictionary of users from the users.json file."""
    try:  # Begins a try block to handle potential file errors.
        with open(USER_DATA_FILE, 'r') as f:  # Opens the user data file in read mode ('r').
            return json.load(f)  # Reads the JSON content from the file and returns it as a Python dictionary.
    except (IOError, json.JSONDecodeError):  # Catches file read errors or if the JSON is invalid.
        return {}  # Returns an empty dictionary if the file is missing or corrupted.


# Function to save user data to the JSON file.
def save_users(users):
    """Saves a dictionary of users to the users.json file."""
    with open(USER_DATA_FILE, 'w') as f:  # Opens the user data file in write mode, overwriting existing content.
        json.dump(users, f,
                  indent=4)  # Writes the 'users' dictionary to the file. 'indent=4' makes the file human-readable.


# ---------------------------------
# 2.2 INPUT BOX CLASS
# ---------------------------------
class InputBox:
    """A class to create and manage a user text input box."""

    def __init__(self, x, y, w, h, placeholder='',
                 is_password=False):  # The constructor method to initialize a new InputBox object.
        self.rect = pygame.Rect(x, y, w, h)  # Creates a rectangle object for the input box's position and size.
        self.color = (255, 255, 255)  # Sets the default color of the input box border (white).
        self.text = ''  # Initializes the user-entered text as an empty string.
        self.placeholder = placeholder  # Stores the placeholder text to show when the box is empty.
        self.font = pygame.font.Font(None, 40)  # Sets the font for the text inside the box.
        self.txt_surface = self.font.render(self.placeholder, True, self.color)  # Renders the initial placeholder text.
        self.active = False  # A flag to track if the user is currently typing in this box.
        self.is_password = is_password  # A flag to determine if the text should be hidden (for passwords).

    def handle_event(self, event):
        """Handles events for the input box (mouse clicks and key presses)."""
        if event.type == pygame.MOUSEBUTTONDOWN:  # Checks if the event is a mouse click.
            if self.rect.collidepoint(event.pos):  # Checks if the mouse click was inside the input box's rectangle.
                self.active = True  # Activates the input box.
            else:
                self.active = False  # Deactivates the input box if the click was outside.
        if event.type == pygame.KEYDOWN:  # Checks if the event is a key press.
            if self.active:  # Only processes key presses if the box is active.
                if event.key == pygame.K_RETURN:  # If the Enter key is pressed.
                    return self.text  # Returns the current text (used for submission).
                elif event.key == pygame.K_BACKSPACE:  # If the Backspace key is pressed.
                    self.text = self.text[:-1]  # Removes the last character from the text string.
                else:
                    self.text += event.unicode  # Appends the typed character to the text string.
        return None  # Returns None if the Enter key wasn't pressed.

    def draw(self, screen):
        """Draws the input box on the screen."""
        display_text = '*' * len(
            self.text) if self.is_password else self.text or self.placeholder  # Determines what text to show: asterisks for password, user text, or placeholder.
        self.txt_surface = self.font.render(display_text, True, self.color)  # Renders the determined text.
        screen.blit(self.txt_surface,
                    (self.rect.x + 5, self.rect.y + 5))  # Draws the text surface onto the screen, slightly padded.
        pygame.draw.rect(screen, self.color, self.rect, 2)  # Draws the border of the input box.


# ---------------------------------
# 2.3 BUTTON DRAW FUNCTION
# ---------------------------------
def draw_button(text, x, y, w, h):
    """Draws a clickable button and returns its rectangle."""
    rect = pygame.Rect(x, y, w, h)  # Creates a rectangle for the button's position and size.
    pygame.draw.rect(screen, (0, 100, 200), rect,
                     border_radius=8)  # Draws the button's background with rounded corners.
    txt_surface = text_font.render(text, True, (255, 255, 255))  # Renders the text for the button.
    screen.blit(txt_surface, (x + w // 2 - txt_surface.get_width() // 2,
                              y + h // 2 - txt_surface.get_height() // 2))  # Draws the text centered on the button.
    return rect  # Returns the button's rectangle, used to check for clicks.


# ===================================================================================
# SECTION 3: GAME SCREENS AND STATES
# This section contains the functions that define the different screens of the game,
# such as the login screen, start menu, and game over screen.
# ===================================================================================

# ---------------------------------
# 3.1 LOGIN SCREEN
# ---------------------------------
def login_screen():
    """Displays the login/register screen and handles user authentication."""
    username_box = InputBox(WIDTH // 2 - 150, HEIGHT // 2 - 70, 300, 50,
                            'Username')  # Creates an input box for the username.
    password_box = InputBox(WIDTH // 2 - 150, HEIGHT // 2, 300, 50, 'Password',
                            is_password=True)  # Creates a password input box.
    error = ''  # Initializes an empty string to hold any error messages.
    clock = pygame.time.Clock()  # Creates a clock object to control the screen's frame rate.

    while True:  # The main loop for the login screen.
        screen.blit(background, (0, 0))  # Draws the background image.

        panel_surface = pygame.Surface((400, 320),
                                       pygame.SRCALPHA)  # Creates a new surface for a semi-transparent panel.
        panel_surface.fill((0, 0, 0, 180))  # Fills the panel with black color at 180/255 transparency.
        screen.blit(panel_surface, (WIDTH // 2 - 200, HEIGHT // 2 - 140))  # Draws the panel onto the screen.

        title = title_font.render("EXODUS LOGIN", True, (0, 255, 0))  # Renders the login screen title.
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2,
                            HEIGHT // 2 - 200))  # Draws the title centered at the top of the panel.

        username_box.draw(screen)  # Draws the username input box.
        password_box.draw(screen)  # Draws the password input box.

        users = load_users()  # Loads the current user data from the file.
        username_text = username_box.text.strip()  # Gets the text from the username box, removing leading/trailing whitespace.
        if username_text in users:  # Checks if the entered username exists in the user data.
            last_score = users[username_text].get('last_score',
                                                  0)  # Gets the last score for that user, defaulting to 0.
            high_score_val = users[username_text].get('high_score',
                                                      0)  # Gets the high score for that user, defaulting to 0.
            last_score_text = small_font.render(f"Last Score: {last_score}", True,
                                                (255, 255, 255))  # Renders the last score text.
            high_score_text = small_font.render(f"High Score: {high_score_val}", True,
                                                (255, 255, 0))  # Renders the high score text.
            screen.blit(last_score_text,
                        (WIDTH // 2 - last_score_text.get_width() // 2, HEIGHT // 2 + 60))  # Draws the last score text.
            screen.blit(high_score_text,
                        (WIDTH // 2 - high_score_text.get_width() // 2, HEIGHT // 2 + 95))  # Draws the high score text.

        login_btn = draw_button("Login", WIDTH // 2 - 160, HEIGHT // 2 + 140, 150, 50)  # Draws the login button.
        register_btn = draw_button("Register", WIDTH // 2 + 10, HEIGHT // 2 + 140, 150,
                                   50)  # Draws the register button.

        if error:  # Checks if there is an error message to display.
            err_txt = small_font.render(error, True, (255, 50, 50))  # Renders the error message in red.
            screen.blit(err_txt, (WIDTH // 2 - err_txt.get_width() // 2,
                                  HEIGHT // 2 + 210))  # Draws the error message below the buttons.

        for event in pygame.event.get():  # Starts the event handling loop.
            if event.type == pygame.QUIT:  # Checks if the user clicked the window's close button.
                pygame.quit()  # Uninitializes Pygame.
                exit()  # Exits the script.
            if event.type == pygame.KEYDOWN:  # Checks for a key press.
                if event.key == pygame.K_ESCAPE:  # If the escape key is pressed.
                    pygame.quit()  # Uninitializes Pygame.
                    exit()  # Exits the script.

            username_box.handle_event(event)  # Passes the event to the username box to handle.
            password_box.handle_event(event)  # Passes the event to the password box to handle.

            if event.type == pygame.MOUSEBUTTONDOWN:  # Checks for a mouse click.
                if login_btn.collidepoint(event.pos):  # Checks if the click was on the login button.
                    username = username_box.text.strip()  # Gets the entered username.
                    password = password_box.text.strip()  # Gets the entered password.
                    if username in users and users[username][
                        'password'] == password:  # Checks if the username exists and the password matches.
                        return username, users[username].get('high_score',
                                                             0)  # Returns the username and high score on successful login.
                    else:
                        error = "Invalid username or password."  # Sets an error message for failed login.

                elif register_btn.collidepoint(event.pos):  # Checks if the click was on the register button.
                    username = username_box.text.strip()  # Gets the entered username.
                    password = password_box.text.strip()  # Gets the entered password.
                    if not username or not password:  # Checks if either field is empty.
                        error = "Username and password required."  # Sets an error message.
                    elif username in users:  # Checks if the username is already taken.
                        error = "Username already exists."  # Sets an error message.
                    else:
                        users[username] = {'password': password, 'high_score': 0,
                                           'last_score': 0}  # Creates a new entry for the user.
                        save_users(users)  # Saves the updated user data to the file.
                        return username, 0  # Returns the new username and a high score of 0.

        pygame.display.flip()  # Updates the full display Surface to the screen.
        clock.tick(30)  # Limits the login screen to 30 frames per second.


# ---------------------------------
# 3.2 IN-GAME UI FUNCTIONS
# ---------------------------------
def show_info():
    """Displays the score, high score, and lives at the top of the screen."""
    pygame.draw.rect(screen, (10, 10, 10, 200), (0, 0, WIDTH, 40))  # Draws a semi-transparent black bar at the top.
    pygame.draw.line(screen, (255, 255, 255), (0, 40), (WIDTH, 40), 2)  # Draws a white line below the bar.
    screen.blit(font.render(f"Score: {score}", True, (255, 255, 255)), (30, 10))  # Renders and draws the current score.
    screen.blit(font.render(f"High Score: {high_score}", True, (255, 215, 0)),
                (WIDTH // 2 - 100, 10))  # Renders and draws the high score in gold.
    screen.blit(font.render(f"Lives: {lives}", True, (0, 255, 0)),
                (WIDTH - 180, 10))  # Renders and draws the remaining lives in green.


# ---------------------------------
# 3.3 START SCREEN
# ---------------------------------
def show_start_screen():
    """Draws the start screen where the player selects the difficulty."""
    title = title_font.render("EXODUS", True, (0, 255, 0))  # Renders the main game title.
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2,
                        HEIGHT // 2 - 200))  # Draws the title in the upper-middle of the screen.
    easy_btn = draw_button("1 - Easy", WIDTH // 2 - 100, HEIGHT // 2 - 60, 200,
                           50)  # Draws the 'Easy' difficulty button.
    medium_btn = draw_button("2 - Medium", WIDTH // 2 - 100, HEIGHT // 2 + 10, 200,
                             50)  # Draws the 'Medium' difficulty button.
    hard_btn = draw_button("3 - Hard", WIDTH // 2 - 100, HEIGHT // 2 + 80, 200,
                           50)  # Draws the 'Hard' difficulty button.
    return easy_btn, medium_btn, hard_btn  # Returns the rectangles of the buttons for click detection.


# ---------------------------------
# 3.4 GAME OVER SCREEN
# ---------------------------------
def show_game_over():
    """Displays the game over message and restart instructions."""
    over_font = pygame.font.Font(None, 80)  # Creates a large font for the "GAME OVER" text.
    restart_font = pygame.font.Font(None, 50)  # Creates a smaller font for the restart instruction.
    over_text = over_font.render("GAME OVER", True, (255, 0, 0))  # Renders the "GAME OVER" text in red.
    restart_text = restart_font.render("Press 'R' to Restart", True,
                                       (255, 255, 255))  # Renders the restart text in white.
    screen.blit(over_text,
                (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2 - 50))  # Draws the "GAME OVER" text centered.
    screen.blit(restart_text,
                (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))  # Draws the restart text below it.


# ===================================================================================
# SECTION 4: CORE GAME LOGIC AND VARIABLES
# This section defines all the variables that control the state of the game
# (player position, score, etc.) and the core functions for gameplay mechanics.
# ===================================================================================

# ---------------------------------
# 4.1 GAME STATE AND DIFFICULTY
# ---------------------------------
START, PLAYING, GAME_OVER = "START", "PLAYING", "GAME_OVER"  # Defines constants for the different game states.
game_state = START  # Sets the initial game state to the start screen.

difficulty_settings = {  # A dictionary containing settings for each difficulty level.
    "Easy": {"num_aliens": 20, "alien_speed": 4, "alien_drop": 50},  # Settings for Easy mode.
    "Medium": {"num_aliens": 40, "alien_speed": 6, "alien_drop": 60},  # Settings for Medium mode.
    "Hard": {"num_aliens": 60, "alien_speed": 8, "alien_drop": 70}  # Settings for Hard mode.
}
current_difficulty = {}  # An empty dictionary to hold the settings for the currently selected difficulty.

# ---------------------------------
# 4.2 PLAYER VARIABLES
# ---------------------------------
playerX = WIDTH // 2  # Sets the player's initial X position to the center of the screen.
playerY = HEIGHT - 150  # Sets the player's initial Y position near the bottom of the screen.
playerX_change = 0  # Initializes the player's horizontal speed to 0.
playerY_change = 0  # Initializes the player's vertical speed to 0.
player_speed = 7  # Sets the speed at which the player moves.
player_damaged = False  # A flag to track if the player has recently taken damage.
damage_timer = 0  # A timer to control the duration of the player's invulnerability after being hit.

# ---------------------------------
# 4.3 BULLET VARIABLES
# ---------------------------------
bullets = []  # An empty list to store all active bullet rectangles on the screen.
bulletY_change = 20  # The speed at which bullets travel up the screen.
bullet_delay = 100  # The delay in milliseconds between shots, creating a machine-gun effect.
last_bullet_time = 0  # A timer to track when the last bullet was fired.

# ---------------------------------
# 4.4 ALIEN VARIABLES
# ---------------------------------
alien_width, alien_height = 60, 60  # Defines the width and height of the alien sprites.
aliens = []  # An empty list to store all active alien objects.

# ---------------------------------
# 4.5 SCORE AND LIVES
# ---------------------------------
score = 0  # Initializes the player's score for the current game to 0.
high_score = 0  # Initializes the high score display, which will be updated after login.
lives = 3  # Sets the number of lives the player starts with.
font = pygame.font.Font(None, 35)  # Re-initializes a font object for the info bar.


# ---------------------------------
# 4.6 CORE GAMEPLAY FUNCTIONS
# ---------------------------------
def spawn_initial_aliens(num):
    """Creates the initial wave of aliens based on the chosen difficulty."""
    global aliens  # Declares that this function will modify the global 'aliens' list.
    aliens.clear()  # Removes any aliens from previous games.
    for _ in range(num):  # Loops 'num' times to create the specified number of aliens.
        aliens.append({  # Appends a new alien dictionary to the list.
            'rect': pygame.Rect(random.randint(0, WIDTH - alien_width), random.randint(50, 300), alien_width,
                                alien_height),  # Creates a rectangle for the alien at a random position.
            'x_change': random.choice([-current_difficulty['alien_speed'], current_difficulty['alien_speed']])
            # Assigns a random horizontal direction and speed.
        })


def player(x, y):
    """Draws the player's spaceship on the screen."""
    screen.blit(player_img, (x, y))  # `blit` is used to draw one image onto another.


def alien(x, y):
    """Draws an alien on the screen."""
    screen.blit(alien_img, (x, y))  # Draws the alien image at the specified x, y coordinates.


# ===================================================================================
# SECTION 5: MAIN GAME EXECUTION
# This is where the game starts. It runs the login screen and then enters the
# main game loop, which controls the flow of the entire game.
# ===================================================================================

# ---------------------------------
# 5.1 PRE-GAME LOGIN
# ---------------------------------
user_info = login_screen()  # Calls the login screen function, which runs until a user logs in or registers.
if user_info is None:  # If the login screen was closed without a successful login.
    pygame.quit()  # Uninitialize Pygame.
    exit()  # Exit the script.
else:
    username, high_score = user_info  # Unpacks the returned username and high score.

# ---------------------------------
# 5.2 MAIN GAME LOOP
# ---------------------------------
clock = pygame.time.Clock()  # Creates a clock object to manage the game's frame rate.
running = True  # The main flag that keeps the game loop running.

while running:  # The heart of the game; this loop runs continuously until 'running' is set to False.
    screen.blit(background, (0, 0))  # Redraws the background image on every frame, clearing the previous frame.
    current_time = pygame.time.get_ticks()  # Gets the current time in milliseconds since Pygame was initialized.

    # --- Event Handling ---
    for event in pygame.event.get():  # Processes the queue of all user input events.
        if event.type == pygame.QUIT:  # Checks if the user has clicked the window's close button.
            running = False  # Sets the running flag to False to exit the main loop.

        if event.type == pygame.KEYDOWN:  # Checks if a key has been pressed down.
            if event.key == pygame.K_ESCAPE:  # Checks if the pressed key was the Escape key.
                running = False  # Exits the main loop.

            if game_state == GAME_OVER and event.key == pygame.K_r:  # If the game is over and the 'R' key is pressed.
                game_state = START  # Resets the game state to the start screen.
                score = 0  # Resets the score.
                lives = 3  # Resets the lives.
                playerX = WIDTH // 2  # Resets the player's position.
                playerY = HEIGHT - 150  # Resets the player's position.
                bullets.clear()  # Clears any bullets left on the screen.

            elif game_state == PLAYING:  # Handles key presses only when in the 'PLAYING' state.
                if event.key == pygame.K_a: playerX_change = -player_speed  # Moves left.
                if event.key == pygame.K_d: playerX_change = player_speed  # Moves right.
                if event.key == pygame.K_w: playerY_change = -player_speed  # Moves up.
                if event.key == pygame.K_s: playerY_change = player_speed  # Moves down.

        if event.type == pygame.KEYUP and game_state == PLAYING:  # Checks if a key has been released.
            if event.key in [pygame.K_a, pygame.K_d]: playerX_change = 0  # Stops horizontal movement.
            if event.key in [pygame.K_w, pygame.K_s]: playerY_change = 0  # Stops vertical movement.

        if game_state == START:  # Handles events only when on the start screen.
            easy_btn, medium_btn, hard_btn = show_start_screen()  # Redraws buttons to get their latest rects.
            if event.type == pygame.MOUSEBUTTONDOWN:  # Checks for a mouse click.
                if easy_btn.collidepoint(event.pos):
                    difficulty = "Easy"  # Sets difficulty to Easy.
                elif medium_btn.collidepoint(event.pos):
                    difficulty = "Medium"  # Sets difficulty to Medium.
                elif hard_btn.collidepoint(event.pos):
                    difficulty = "Hard"  # Sets difficulty to Hard.
                else:
                    continue  # If the click wasn't on a button, ignore it and continue the loop.

                current_difficulty = difficulty_settings[difficulty]  # Loads the settings for the chosen difficulty.
                spawn_initial_aliens(current_difficulty['num_aliens'])  # Creates the first wave of aliens.
                game_state = PLAYING  # Changes the game state to start the gameplay.

    # --- Game State Logic ---
    if game_state == START:  # If the game is in the 'START' state.
        show_start_screen()  # Continuously draw the start screen.

    elif game_state == PLAYING:  # If the game is in the 'PLAYING' state.
        # Player Logic
        playerX += playerX_change  # Updates the player's X position based on their speed.
        playerY += playerY_change  # Updates the player's Y position based on their speed.
        player_rect = pygame.Rect(playerX, playerY, 60, 60)  # Creates a rectangle for the player's current position.
        player_rect.clamp_ip(screen.get_rect())  # Prevents the player from moving off-screen.
        playerX, playerY = player_rect.x, player_rect.y  # Updates the player's coordinates after clamping.
        player(playerX, playerY)  # Draws the player at the new position.

        if player_damaged:  # Checks if the player is in a damaged state.
            if current_time - damage_timer < 300:  # If it's been less than 300ms since being hit.
                if current_time % 100 < 50:  # Creates a blinking effect by only drawing the damage indicator half the time.
                    pygame.draw.rect(screen, (255, 0, 0, 150), player_rect,
                                     4)  # Draws a red rectangle around the player.
            else:
                player_damaged = False  # Ends the damaged state after 300ms.

        # Bullet Logic
        keys = pygame.key.get_pressed()  # Gets the state of all keyboard keys.
        if keys[pygame.K_SPACE]:  # Checks if the spacebar is being held down.
            if current_time - last_bullet_time > bullet_delay:  # Checks if enough time has passed since the last shot.
                last_bullet_time = current_time  # Resets the bullet timer.
                bullet_rect = pygame.Rect(playerX + 20, playerY, bullet_img.get_width(),
                                          bullet_img.get_height())  # Creates a new bullet rectangle at the player's position.
                bullets.append(bullet_rect)  # Adds the new bullet to the list of active bullets.

        for bullet in bullets[:]:  # Loops through a copy of the bullets list (to allow removing items while iterating).
            bullet.y -= bulletY_change  # Moves the bullet up the screen.
            if bullet.bottom < 0:  # Checks if the bullet has gone off the top of the screen.
                bullets.remove(bullet)  # Removes the bullet from the list.
            else:
                screen.blit(bullet_img, bullet)  # Draws the bullet at its new position.

        # Alien Logic
        for alien_obj in aliens[:]:  # Loops through a copy of the aliens list.
            alien_obj['rect'].x += alien_obj['x_change']  # Moves the alien horizontally.

            if alien_obj['rect'].left <= 0 or alien_obj[
                'rect'].right >= WIDTH:  # Checks if the alien hit the side of the screen.
                alien_obj['x_change'] *= -1  # Reverses the alien's horizontal direction.
                alien_obj['rect'].y += current_difficulty['alien_drop']  # Moves the alien down.

            # Collision Detection
            if player_rect.colliderect(alien_obj['rect']):  # Checks for a collision between the player and an alien.
                if not player_damaged:  # Only processes the collision if the player is not already in a damaged state.
                    lives -= 1  # Decrements the player's lives.
                    player_damaged = True  # Puts the player in a damaged state.
                    damage_timer = current_time  # Starts the invulnerability timer.
                    aliens.remove(alien_obj)  # Removes the alien that hit the player.

            for bullet in bullets[:]:  # Nested loop to check each bullet against the current alien.
                if bullet.colliderect(alien_obj['rect']):  # Checks for a collision between a bullet and the alien.
                    score += 10  # Increases the player's score.
                    if alien_obj in aliens: aliens.remove(alien_obj)  # Removes the hit alien.
                    bullets.remove(bullet)  # Removes the bullet that hit the alien.
                    aliens.append({  # Spawns a new alien to replace the one that was destroyed.
                        'rect': pygame.Rect(random.randint(0, WIDTH - alien_width), random.randint(50, 150),
                                            alien_width, alien_height),
                        'x_change': random.choice(
                            [-current_difficulty['alien_speed'], current_difficulty['alien_speed']])
                    })
                    break  # Exits the inner bullet loop since this bullet is gone.

            if alien_obj in aliens and alien_obj[
                'rect'].bottom > HEIGHT:  # Checks if an alien has reached the bottom of the screen.
                lives = 0  # The player loses immediately.

            if alien_obj in aliens:  # Checks if the alien still exists (it might have been removed).
                alien(alien_obj['rect'].x, alien_obj['rect'].y)  # Draws the alien.

        # Game Over Check
        if lives <= 0:  # Checks if the player has run out of lives.
            users = load_users()  # Loads the user data.
            users[username]['last_score'] = score  # Updates the user's last score.
            if score > users[username].get('high_score', 0):  # Checks if the current score is a new high score.
                users[username]['high_score'] = score  # Updates the high score.
                high_score = score  # Updates the high score variable for the info bar.
            save_users(users)  # Saves the updated scores to the file.
            game_state = GAME_OVER  # Changes the game state to 'GAME_OVER'.

        show_info()  # Draws the information bar at the top of the screen.

    elif game_state == GAME_OVER:  # If the game is in the 'GAME_OVER' state.
        show_game_over()  # Continuously draw the game over screen.

    pygame.display.update()  # Updates the screen to show all the changes made in this frame.
    clock.tick(60)  # Pauses the game long enough to ensure it doesn't exceed 60 frames per second.

# ---------------------------------
# 5.3 CLEANUP
# ---------------------------------
pygame.quit()  # Uninitializes all Pygame modules when the main loop ends.
