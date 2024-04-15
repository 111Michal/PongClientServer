import socket # biblioteka z narzędziami do komunikacji sieciowej, gniazda, protokoły itp.
import constants as cn # import stałych

# klasa obsługująca funkcje sieciowe w kliencie
class Network:
    def __init__(self): # konstruktor
        # socket.AF_INET określa rodzaj adresu ip, którego będzie używało gniazdo -> tutaj jest to w formie IPv4 np. '127.0.0.1'
        # socket.SOCK_STREAM określa rodzaj gniazda, w tym wypadku dane będą wysyłane w formie strumienia bajtów (TCP)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = cn.IP # adres IP serwera
        self.port = cn.PORT # port na którym odbędzie się komunikacja
        self.addr = (self.server, self.port) # zmienna przechowująca ip serwera oraz port

    # metoda do połączenia się z serwerem
    def connect(self):
        try:
            # nawiązanie połączenia z serwerem, używając adresu i portu zdefiniowanych w konstruktorze
            self.client.connect(self.addr)
            # otrzymanie danych od serwera po połączeniu i zwrócenie ich po dekodowaniu z bajtów do łańcucha znaków
            # pozwala na natychmiastowe pobranie danych startowych od serwera
            return self.client.recv(2048).decode()
        except:
            pass

    # metoda pozwalająca na jednoczesne wysłanie oraz odebranie danych do/z serwera
    def send(self, data):
        try:
            # próba wysłania danych do serwera po zakodowaniu ich do postaci bajtowej.
            self.client.send(str.encode(data))
            # otrzymanie danych od serwera po wysłaniu wiadomości i zwrócenie ich po dekodowaniu z bajtów do łańcucha znaków.
            return self.client.recv(2048).decode()
        except socket.error as e: # wychwycenie błędu
            print(e)
