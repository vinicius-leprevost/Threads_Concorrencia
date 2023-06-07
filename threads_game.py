import threading
import time
import random

class Cofre:
    def __init__(self, max_senha=99999999):
        self._senha = str(random.randint(0, max_senha))

    def get_senha(self):
        return self._senha

    def tentar_abrir(self, tentativa):
        return self._senha == tentativa

class Hacker(threading.Thread):
    def __init__(self, id, cofre, flag_descoberto):
        super().__init__()
        self.id = id
        self.cofre = cofre
        self.flag_descoberto = flag_descoberto
        self.tentativas = 0

    def run(self):
        tentativa = "0"
        while not self.flag_descoberto.is_set():
            if self.cofre.tentar_abrir(tentativa):
                print(f"Hacker {self.id} abriu o cofre!")
                self.flag_descoberto.set()
                break
            else:
                tentativa = str(int(tentativa) + 1)
                self.tentativas += 1

class Policial(threading.Thread):
    def __init__(self, flag_descoberto):
        super().__init__()
        self.flag_descoberto = flag_descoberto

    def run(self):
        for i in range(10, -1, -1):
            if not self.flag_descoberto.is_set():
                print(f"Policial chegará em {i} segundos...")
                time.sleep(1)
            else:
                break
        if not self.flag_descoberto.is_set():
            print("Policial chegou! Hackers presos!")

# Inicializadores
cofre = Cofre()
flag_descoberto = threading.Event()

# Número de threads de hackers
num_threads = 3

# Threads dos hackers
hackers = [Hacker(i, cofre, flag_descoberto) for i in range(num_threads)]

# Grava a hora de início
inicio = time.time()

# Inicialização das threads dos hackers
for hacker in hackers:
    hacker.start()

# Criação e inicialização da thread do policial
Policial(flag_descoberto).start()

# Aguarda terminar...
for hacker in hackers:
    hacker.join()

# Grava hora final
fim = time.time()

total_tentativas = sum(hacker.tentativas for hacker in hackers)
print(f"Número de tentativas: {total_tentativas}")
print(f"Senha Inicial: {cofre.get_senha()}")
print(f"Threads utilizados: {len(hackers)}")
print(f"Tempo de execução: {fim - inicio} segundos")
