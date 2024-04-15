import pygame  # -> import biblioteki pygame, pozwala tworzyć proste gry 2d
import constants as cn  # -> import pliku constants


# klasa piłki
class Ball:
    def __init__(self, color, x, y, radius, x_vel, y_vel):  # konstruktor
        self.color = color  # kolor piłki
        self.x_vel = x_vel  # prędkość piłki współrzędnej x
        self.y_vel = y_vel  # prędkość piłki współrzędnej y
        self.x_vel_start = x_vel  # prędkość startowa piłki współrzędnej x
        self.y_vel_start = y_vel  # prędkość startowa piłki współrzędnej y
        self.x = x  # położenie piłki x
        self.y = y  # położenie piłki y
        self.radius = radius  # promień piłki
        self.circle = (x, y, radius)  # tuple do stworzenia piłki jako koła
        self.right_points = 0  # liczba punktów gracza po prawej
        self.left_points = 0  # liczba punktów gracza po lewej

    def wall_collide(self):  # obsługa kolizji ze ścianami
        if self.y <= 0 + self.radius or self.y >= cn.HEIGHT - self.radius:  # kolizja z górną lub dolną ścianą
            self.y_vel *= -1  # zmiana kierunku lotu piłki
        if self.x >= cn.WIDTH - self.radius:  # kolizja z prawą stroną ekranu
            self.x, self.y = cn.WIDTH / 2 - self.radius, cn.HEIGHT / 2 - self.radius  # ustawienie pozycji początkowej
            self.y_vel *= -1  # zmiana kierunku lotu piłki x
            self.x_vel *= -1  # zmiana kierunku lotu piłki y

            self.left_points += 1  # dodanie punktu graczowi po lewej stronie
        if self.x <= 0 + self.radius:  # kolizja z lewą stroną ekranu
            self.x, self.y = cn.WIDTH / 2 - self.radius, cn.HEIGHT / 2 - self.radius # ustawienie pozycji początkowej
            self.x_vel, self.y_vel = self.x_vel_start, self.y_vel_start # reset lotu piłki

            self.right_points += 1 # dodanie punktu graczowi po prawej stronie

    def paddle_collide(self, left_paddle_pos, right_paddle_pos): # kolizja piłki z paletką
        left_paddle_x, left_paddle_y = left_paddle_pos # rozdzielenie na składową x i y
        if self.circle[0] - self.radius < left_paddle_x + cn.PADDLE_WIDTH and \
                self.circle[1] + self.radius > left_paddle_y and \
                self.circle[1] - self.radius < left_paddle_y + cn.PADDLE_HEIGHT: # kolizja piłki z lewą paletką

            self.x_vel *= -1 # zmiana kierunku składowej x piłki

        right_paddle_x, right_paddle_y = right_paddle_pos # rozdzielenie na składową x i y
        if self.circle[0] + self.radius > right_paddle_x and \
                self.circle[1] + self.radius > right_paddle_y and \
                self.circle[1] - self.radius < right_paddle_y + cn.PADDLE_HEIGHT: # kolizja piłki z prawą paletką

            self.x_vel *= -1 # zmiana kierunku składowej x piłki

    def move(self): # ruch piłki
        self.x += self.x_vel # przesuwanie po x
        self.y += self.y_vel # przeysuwanie po y
        self.update() # wywołanie metody update()

    def draw(self, window): # rysowanie
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius) # wykorzystanie funkcji circle do narysowania okręgu

    def update(self):
        self.circle = (self.x, self.y, self.radius) # aktualizacja zmiennych po ruchu
