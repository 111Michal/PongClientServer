import pygame  # -> import biblioteki pygame, pozwala tworzyć proste gry 2d
import constants as cn  # -> import pliku constants

pygame.font.init()  # załadowanie domyślnych czcionek z pygame


# klasa tekstu -> wyświetla punkty
class Points:
    def __init__(self, size, left_points, right_points):  # konstruktor
        self.left_points = left_points  # liczba punktów zebranych przez lewego gracza
        self.right_points = right_points  # liczba punktów zebranych przez prawego gracza
        self.font = pygame.font.Font(None, size)  # załadowanie czcionki

    def draw(self, win):  # rysowanie
        text = self.font.render(f"{self.left_points} : {self.right_points}", True, cn.WHITE)  # renderowanie tekstu
        text_rect = text.get_rect(center=(win.get_width() // 2, 20))  # ustawienie tekstu na środku i na górze
        win.blit(text, text_rect.topleft)  # umieszczenie tekstu na oknie gry
