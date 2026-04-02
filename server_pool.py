import socket
import time
from concurrent.futures import ThreadPoolExecutor
import threading


class ThreadPoolHTTPServer:
    def __init__(self, host='localhost', port=8080, max_workers=3):
        self.host = host
        self.port = port
        self.max_workers = max_workers
        self.server_socket = None
        self.executor = None
        self.running = False
        self.active_connections = 0
        self.total_processed = 0
        self.lock = threading.Lock()

    def handle_client(self, client_socket, client_address):
        """Обработка клиентского запроса"""
        with self.lock:
            self.active_connections += 1
            active = self.active_connections

        try:
            thread_name = threading.current_thread().name
            print(f"\n[⟳] Обслуживается {client_address}")
            print(f"    Поток: {thread_name} (пул: {self.max_workers})")
            print(f"    Активно: {active}, Всего: {self.total_processed}")

            request_data = client_socket.recv(1024)
            print(f"    Запрос: {request_data.decode('utf-8', errors='ignore').split(chr(10))[0]}")

            print(f"    ⏳ Имитация задержки 10 сек...")
            time.sleep(10)

            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            response_body = f"""<!DOCTYPE html>
<html>
<head>
    <title>Thread Pool HTTP Server</title>
    <style>
        body {{ font-family: monospace; margin: 40px; background: #1e1e1e; color: #f0f0f0; }}
        .container {{ background: #2d2d2d; padding: 20px; border-radius: 8px; }}
        .info {{ margin: 10px 0; padding: 8px; background: #3d3d3d; border-radius: 4px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 HTTP Echo Server (Thread Pool)</h1>
        <div class="info">
            <strong>Статистика пула:</strong><br>
            Размер пула: {self.max_workers}<br>
            Активных подключений: {active}<br>
            Всего обработано: {self.total_processed}
        </div>
        <div class="info">
            <strong>Информация о запросе:</strong><br>
            Поток: {thread_name}<br>
            Время: {timestamp}<br>
            Ваш IP: {client_address[0]}:{client_address[1]}
        </div>
        <p>✅ Запрос успешно обработан</p>
    </div>
</body>
</html>"""

            response = (
                f"HTTP/1.1 200 OK\r\n"
                f"Content-Type: text/html; charset=utf-8\r\n"
                f"Content-Length: {len(response_body.encode('utf-8'))}\r\n"
                f"Connection: close\r\n"
                f"\r\n"
                f"{response_body}"
            )

            client_socket.send(response.encode('utf-8'))

            with self.lock:
                self.total_processed += 1

            print(f"[✓] Готово: {client_address}")

        except Exception as e:
            print(f"[✗] Ошибка: {e}")
        finally:
            client_socket.close()
            with self.lock:
                self.active_connections -= 1

    def start(self):
        """Запуск сервера"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(10)
            self.running = True
            self.executor = ThreadPoolExecutor(max_workers=self.max_workers)

            print(f"\n{'=' * 60}")
            print(f"🚀 HTTP Сервер с Потоковым Пуллом")
            print(f"{'=' * 60}")
            print(f"📍 http://{self.host}:{self.port}")
            print(f"🔧 Потоков в пуле: {self.max_workers}")
            print(f"{'=' * 60}")
            print(f"✨ Работаем, ждём подключений...")
            print(f"⌨️  Ctrl+C для остановки\n")

            while self.running:
                try:
                    self.server_socket.settimeout(1)
                    client_socket, client_address = self.server_socket.accept()
                    print(f"[→] Подключился {client_address}")
                    self.executor.submit(self.handle_client, client_socket, client_address)

                except socket.timeout:
                    continue
                except Exception as e:
                    if self.running:
                        print(f"[!] Ошибка: {e}")

        except KeyboardInterrupt:
            print("\n[!] Остановка по Ctrl+C...")
        finally:
            self.shutdown()

    def shutdown(self):
        """Корректное завершение"""
        print("\n[!] Останавливаемся...")
        self.running = False

        if self.executor:
            print("    Ждём завершения задач...")
            self.executor.shutdown(wait=True)
            print("    ✓ Готово")

        if self.server_socket:
            self.server_socket.close()

        print(f"\n📊 Итого обработано: {self.total_processed}")
        print("[✓] Сервер остановлен")


if __name__ == "__main__":
    import sys
    max_workers = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 3

    server = ThreadPoolHTTPServer(max_workers=max_workers)
    server.start()