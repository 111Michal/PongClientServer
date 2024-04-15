import pygame  # -> import biblioteki pygame, pozwala tworzyć proste gry 2d
import constants as cn  # -> import pliku constants


# klasa gracza, czyli paletka #
class Player:
    def __init__(self, x, y, width, height, color, vel):  # konstruktor
        self.x = x  # pozycja x paletki
        self.y = y  # pozycja y paletki
        self.width = width  # szerokość paletki
        self.height = height  # wysokość paletki
        self.color = color  # kolor paletki
        self.rect = (x, y, width, height)  # tuple do stworzenia paletki jako prostokąta
        self.vel = vel  # prędkość paletki

    def draw(self, win):  # rysowanie paletki
        pygame.draw.rect(win, self.color, self.rect)  # wykorzystanie funkcji rect z pygame

    def move(self):  # ruch paletki
        keys = pygame.key.get_pressed()  # wykorzystanie funkcji wykrywającej naciśnięcie klawiszy

        if keys[pygame.K_UP]:  # reakcja na strzałkę w górę
            self.y -= self.vel  # zmiana położenia y, do góry

        if keys[pygame.K_DOWN]:  # reakcja na strzałkę w dół
            self.y += self.vel  # zmiana położenia y, w dół

        self.update()  # wywołanie metody update()

    def wall_collide(self):  # obsługa kolizji ze ścianami
        if self.y >= cn.HEIGHT - self.height:  # zderzenie z dolną krawędzią
            self.y = cn.HEIGHT - self.height  # ustawienie na maksymalne możliwe położenie
        if self.y <= 0:  # zderzenie z górną krawędzią
            self.y = 0  # ustawienie na maksymalne możliwe położenie

    def update(self):  # aktualizacja zmiennych np. po ruchu, lub przyjęciu danych z serwera
        self.rect = (self.x, self.y, self.width, self.height)
