# PLIK SERWERA -> odbiera, wysyła dane od i do klientów, obsługuje ruch piłki

import socket  # biblioteka z narzędziami do komunikacji sieciowej, gniazda, protokoły itp.
from _thread import *  # biblioteka do obsługi wątków
import constants as cn  # stałe
from ball import Ball  # import klasy piłka

server = cn.IP  # adres ip serwera -> ip lokalne
port = cn.PORT  # port na którym odbędzie się połączenie

# socket.AF_INET określa rodzaj adresu ip, którego będzie używało gniazdo -> tutaj jest to w formie IPv4 np. '127.0.0.1'
# socket.SOCK_STREAM określa rodzaj gniazda, w tym wypadku dane będą wysyłane w formie strumienia bajtów (TCP)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))  # Próba przypisania adresu i portu do gniazda 's'
except socket.error as e:
    str(e)  # W przypadku błędu, pobierz komunikat błędu

s.listen(
    2)  # nasłuchiwanie na połączenia, z maksymalnie dwoma oczekującymi połączeniami w kolejce, zakładam dwóch klientów
print("Czekam na połączenie, serwer wystartował")


# funkcja read_pos konwertuje dane, które przyjdą w formacie "x,y" jako łańcuch znaków, potrzebna jest konwersja do int
def read_pos(str):
    str = str.split(",")  # rozdziela łańcuch znaków na listę elementów, używając przecinka jako separatora
    return int(str[0]), int(str[1])  # konwertuje elementy listy (po rozbiciu) na liczby całkowite i zwraca krotkę


# funkcja make_data tworzy dane do wysłania, konwertuje krotki do łańcucha znaków, oddzielając je przecinkami
# dane będą wyglądały tak: "a,b,c,d,e,f"
# tup, tup1 oraz tup2 wygląda tak: (x, y)
def make_data(tup, tup1, tup2):
    return str(tup[0]) + "," + str(tup[1]) + "," + str(tup1[0]) + "," + str(tup1[1]) + "," + str(tup2[0]) + "," + str(
        tup2[1])


positions = [cn.LEFT_PADDLE, cn.RIGHT_PADDLE, cn.BALL]  # zebranie wszystkich pozycji startowych, paletek i piłki
start_points = (cn.LEFT_POINTS, cn.RIGHT_POINTS)  # stworzenie tuple dla liczby punktów lewego i prawego gracza
ball = Ball(cn.RED, positions[2][0], positions[2][1], cn.RADIUS, cn.X_VEL,
            cn.Y_VEL)  # tworzenie obiektu piłki, to serwer kontroluje kolizje piłki z paletkami


# tutaj znajduje się funkcja do komunikacji z klientem, wywołuje się ją w wątku
# każdy klient ma tak jakby swoją instancję tej funkcji w oddzielnym wątku
def threaded_client(conn, player):
    # na początku wysyłane są pozycje startowe, paletki, piłki oraz liczby punktów, zmienna player informuje o numerze klienta
    # dzięki temu można rozróżnić jaką pozycję startową otrzyma gracz po lewej oraz po prawej stronie
    # conn.send() -> wysyła dane przez gniazdo conn
    # str.encode() -> konwertuje łańcuch znaków na sekwencję bajtów, wymagane do wysyłania danych przez gniazda
    # make_data() -> opisano wyżej
    conn.send(str.encode(make_data(positions[player], positions[2], start_points)))

    while True:  # pętla wieczna, cały czas komunikuje się z klientem
        try:
            # odbieranie pozycji od klienta (pozycja paletki)
            # conn.recv -> metoda do odbierania danych przez gniazdo conn z limitem 2048 bajtów
            # .decode() -> konwertuje dane z sekwencji bajtów na łańcuch znaków
            pos = read_pos(conn.recv(2048).decode())
            positions[
                player] = pos  # po odebraniu świeżej pozycji następuje aktualizacja pozycji, nową pozycję trzeba wysłać do drugiego klienta

            if not pos:  # gdy nie otrzymano pozycji, przerywamy komunikację
                print("Rozłączono")
                break
            else:  # w przeciwnymi razie
                if player == 1:  # sprawdzamy czy mamy do czynienia z klientem podłączonym jako drugi, z indeksem 1
                    reply = positions[0]  # przygotowujemy informację do wysłania do klienta z indeksem 0
                else:  # jeśli indeks jest 0, czyli klient podłączony jako pierwszy
                    reply = positions[1]  # przygotowujemy informację do wysłania do klienta z indeksem 1

            # ten warunek sprawdza czy klient ma indeks 1 czyli podłączył się drugi gracz
            # jeśli tak serwer zaczyna obsługiwać ruch piłki
            if player == 1:
                ball.move()  # ruch piłki
                ball.wall_collide()  # obsługa kolizji ze ścianami
                ball.paddle_collide(positions[0], positions[1])  # obsługa kolizji z paletkami

            # wysłanie klientom pozycji przeciwnika, pozycji piłki, oraz punktów gracza lewego i prawego
            conn.sendall(str.encode(make_data(reply, (ball.x, ball.y), (ball.left_points, ball.right_points))))
        except:
            break

    print("Utracono połączenie")
    conn.close()  # zamknięcie połączenia gniazda


currentPlayer = 0  # nadawanie indeksów klientom

while True:  # pętla wieczna, serwer czeka na klientów
    conn, addr = s.accept()  # akcpetowanie połączenia od klienta
    print("Podłączono do:", addr)

    # Uruchom nowy wątek dla każdego klienta
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1  # inkrementacja indeksu
