import requests
import threading
import time
from datetime import datetime
from typing import List, Dict


class ConcurrentHTTPClient:
    def __init__(self, url='http://localhost:8080', num_clients=10):
        self.url = url
        self.num_clients = num_clients
        self.results = []
        self._lock = threading.Lock()

    def _log_request_start(self, client_id: int) -> None:
        """Логирование начала запроса"""
        timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        print(f"[{timestamp}] Клиент #{client_id:2d}: Отправка запроса...")

    def _log_request_result(self, client_id: int, status_code: int, duration: float) -> None:
        """Логирование результата запроса"""
        timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        print(f"[{timestamp}] Клиент #{client_id:2d}: ✓ Статус {status_code} (⏱️ {duration:.2f} сек)")

    def _save_result(self, client_id: int, status_code: int, duration: float) -> None:
        """Сохранение результата запроса"""
        with self._lock:
            self.results.append({
                'id': client_id,
                'status': status_code,
                'duration': duration
            })

    def send_request(self, client_id: int) -> None:
        """Отправка одного запроса"""
        try:
            start_time = time.time()
            self._log_request_start(client_id)
            
            response = requests.get(self.url, timeout=30)
            duration = time.time() - start_time
            
            self._save_result(client_id, response.status_code, duration)
            self._log_request_result(client_id, response.status_code, duration)

        except Exception as error:
            print(f"[!] Клиент #{client_id}: ✗ Ошибка - {error}")

    def _print_header(self) -> None:
        """Печать заголовка"""
        print(f"\n{'=' * 60}")
        print(f"🚀 Запуск HTTP клиентов")
        print(f"{'=' * 60}")
        print(f"📍 Сервер: {self.url}")
        print(f"👥 Клиентов: {self.num_clients}")
        print(f"{'=' * 60}\n")

    def _print_statistics(self, total_time: float) -> None:
        """Печать статистики"""
        print(f"\n{'=' * 60}")
        print(f"📊 Статистика")
        print(f"{'=' * 60}")
        
        successful = len([r for r in self.results if r['status'] == 200])
        print(f"✅ Успешно: {successful}/{self.num_clients}")

        if self.results:
            durations = [r['duration'] for r in self.results]
            print(f"⏱️  Среднее время: {sum(durations) / len(durations):.2f} сек")
            print(f"🐌 Минимум: {min(durations):.2f} сек")
            print(f"⚡ Максимум: {max(durations):.2f} сек")

        print(f"📦 Общее время: {total_time:.2f} сек")
        print(f"{'=' * 60}")

    def run(self) -> None:
        """Запуск всех клиентов"""
        self._print_header()
        
        start_time = time.time()
        threads = []

        # Запускаем клиентов
        for client_num in range(self.num_clients):
            thread = threading.Thread(target=self.send_request, args=(client_num + 1,))
            thread.daemon = True
            threads.append(thread)
            thread.start()
            time.sleep(0.1)  # Небольшая задержка между запусками

        # Ждем завершения
        for thread in threads:
            thread.join()

        self._print_statistics(time.time() - start_time)


def parse_arguments() -> int:
    """Парсинг аргументов командной строки"""
    import sys
    
    if len(sys.argv) > 1:
        try:
            return int(sys.argv[1])
        except ValueError:
            print("⚠️  Неверное значение, используется значение по умолчанию: 10")
    return 10


if __name__ == "__main__":
    clients_count = parse_arguments()
    client = ConcurrentHTTPClient(num_clients=clients_count)
    client.run()