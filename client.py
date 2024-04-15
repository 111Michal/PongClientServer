# PLIK KLIENTA -> to co obsługuje gracz, czyli poruszanie paletką, natomiast ruch piłki odbywa się z poziomu serwera,
# klient tylko rysuje piłkę na podstawie pozycji uzyskanej od serwera

import pygame  # -> import biblioteki pygame, pozwala tworzyć proste gry 2d
from network import Network  # import pliku z komunikacją sieciową
import constants as cn  # import stałych
from player import Player  # import klasy gracza
from ball import Ball  # import klasy piłki
from points import Points  # import klasy do zliczania punktów

# inicjalizacja okna gry
win = pygame.display.set_mode((cn.WIDTH, cn.HEIGHT))
pygame.display.set_caption("Pong Game")  # ustawienie tytułu

# wczytanie obrazu tła
background_image = pygame.image.load(cn.IMG)  # wczytanie obrazu
background_image = pygame.transform.scale(background_image, (cn.WIDTH, cn.HEIGHT))  # Dopasowanie do rozmiaru okna


# funkcja read_data konwertuje dane, które przyjdą w formacie "a,b,c,d,e,f" jako łańcuch znaków, potrzebna jest konwersja do int oraz float
def read_data(str):
    str = str.split(",")  # rozdziela łańcuch znaków na listę elementów, używając przecinka jako separatora
    return int(str[0]), int(str[1]), float(str[2]), float(str[3]), int(str[4]), int(
        str[5])  # konwertuje elementy listy (po rozbiciu) na liczby całkowite i zwraca krotkę


# funkcja make_pos tworzy dane do wysłania, konwertuje krotki do łańcucha znaków, oddzielając je przecinkami
# dane będą wyglądały tak: "x,y"
# tup wygląda tak: (x, y)
def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])


# funkcja odświeżająca ekran gry, rysuje wszystkie elementy wizualne
def redrawWindow(win, player, player2, ball, points):
    win.blit(background_image, (0, 0))  # wypełnienie tła obrazem
    player.draw(win)
    player2.draw(win)
    ball.draw(win)
    points.draw(win)
    pygame.display.update()  # metoda z pygame do odświeżenia widoku


# funkcja główna gry
def main():
    run = True  # do wiecznej pętli
    n = Network()  # obiekt do komunikacji sieciowej
    data = read_data(
        n.connect())  # budowa metody connect() -> jednocześnie łączy się z serwerem oraz pobiera dane startowe od niego

    # przypisanie starowych zmiennych, odebranych od serwera
    paddle_start_pos = data[0], data[
        1]  # pozycja startowa paletki -> serwer decyduje jaką wysłać, w zależności od indeksu klienta
    ball_start_pos = data[2], data[3]  # pozycja startowa piłki
    left_points = data[4]  # startowa liczba punktów lewego gracza
    right_points = data[5]  # startowa liczba punktów prawego gracza

    # tworzenie obiektów graczy (paletek), piłki i punktów
    p = Player(paddle_start_pos[0], paddle_start_pos[1], cn.PADDLE_WIDTH, cn.PADDLE_HEIGHT, cn.YELLOW, cn.PADDLE_VEL)
    p2 = Player(0, 0, cn.PADDLE_WIDTH, cn.PADDLE_HEIGHT, cn.YELLOW, cn.PADDLE_VEL)
    ball = Ball(cn.RED, ball_start_pos[0], ball_start_pos[1], cn.RADIUS, cn.X_VEL, cn.Y_VEL)
    points = Points(cn.FONT_SIZE, left_points, right_points)

    clock = pygame.time.Clock()  # zegar z biblioteki pygame, pozwala na mierzenie czasu, w tym wypadku do fpsów

    while run:  # pętla wieczna gry
        clock.tick(60)  # 60 klatek na sekundę
        data_loop = read_data(n.send(make_pos((p.x, p.y))))  # odbieranie danych i wysyłanie jednocześnie od/do serwera

        # aktualizacja pozycji drugiego gracza
        p2.x = data_loop[0]  # pozycja x
        p2.y = data_loop[1]  # pozycja y
        p2.update()  # aktualizacja pozycji paletki przeciwnika

        # aktualizacja pozycji piłki
        ball.x = data_loop[2]  # współrzędna x
        ball.y = data_loop[3]  # współrzędna y

        # aktualizacja punktów zdobytych przez graczy
        points.right_points = data_loop[5]  # punkty prawego gracza
        points.left_points = data_loop[4]  # punkty lewego gracza

        for event in pygame.event.get():  # obsługa przycisku wyłączania okna
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        p.move()  # metoda obsługująca ruch gracza
        p.wall_collide()  # metoda obsługująca kolizje gracza ze ścianami
        p2.wall_collide()  # metoda obsługująca kolizje przeciwnika ze ścianami
        redrawWindow(win, p, p2, ball, points)  # wywołanie funkcji do odświeżenia widoku okna


# start funkcji głównej
main()
