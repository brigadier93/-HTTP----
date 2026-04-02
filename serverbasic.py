import socket
import threading
import time


def handle_client(client_socket, client_address):
    """Обработка клиента в отдельном потоке"""
    try:
        print(f"\n[+] Обработка клиента {client_address} в потоке {threading.current_thread().name}")

        # Получаем запрос
        client_socket.recv(1024)

        # Имитация долгой обработки
        print(f"    ⏳ Ожидание 10 секунд...")
        time.sleep(10)

        # Формируем ответ
import socket
import threading
import time


def process_client(client_socket, client_address):
    """Обработка клиента в отдельном потоке"""
    try:
        print(f"\n[+] Обработка клиента {client_address} в потоке {threading.current_thread().name}")

        # Принимаем запрос
        client_socket.recv(1024)

        # Имитация длительной обработки
        print(f"    ⏳ Ожидание 10 секунд...")
        time.sleep(10)

        # Подготавливаем ответ
        response_body = f"""<!DOCTYPE html>
<html>
<body>
    <h1>HTTP Echo Server (Multi-thread)</h1>
    <p>Поток: {threading.current_thread().name}</p>
    <p>Время: {time.strftime('%Y-%m-%d %H:%M:%S')}</p>
    <p>Ваш IP: {client_address[0]}</p>
</body>
</html>"""

        response = (
            f"HTTP/1.1 200 OK\r\n"
            f"Content-Type: text/html\r\n"
            f"Content-Length: {len(response_body.encode('utf-8'))}\r\n"
            f"\r\n"
            f"{response_body}"
        )

        client_socket.send(response.encode('utf-8'))
        print(f"[✓] Ответ отправлен {client_address}")

    except Exception as e:
        print(f"[✗] Ошибка: {e}")
    finally:
        client_socket.close()


def run_server():
    """Запуск сервера"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 8080))
    server_socket.listen(5)

    print(f"\n{'=' * 60}")
    print(f"🚀 Многопоточный HTTP Сервер")
    print(f"{'=' * 60}")
    print(f"📍 Адрес: http://localhost:8080")
    print(f"✨ Сервер запущен")
    print(f"⌨️  Нажмите Ctrl+C для остановки\n")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"[→] Подключение от {client_address}")

            # Запускаем новый поток для каждого клиента
            thread = threading.Thread(
                target=process_client,
                args=(client_socket, client_address)
            )
            thread.daemon = True
            thread.start()

    except KeyboardInterrupt:
        print("\n[!] Остановка сервера...")
    finally:
        server_socket.close()


if __name__ == "__main__":
    run_server()