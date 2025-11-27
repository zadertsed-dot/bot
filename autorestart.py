import os
import sys
import time
from threading import Thread

def init_auto_restart(interval=3600):
    """
    Автоматически перезапускает скрипт через заданный интервал.
    
    Args:
        interval (int): Интервал в секундах (по умолчанию 1 час).
    """
    def restart_loop():
        while True:
            time.sleep(interval)
            print(f"🔄 Перезапуск через {interval} сек...")
            python = sys.executable
            os.execl(python, python, *sys.argv)  # Полная замена процесса
    
    # Запуск в фоновом режиме (daemon=True)
    Thread(target=restart_loop, daemon=True).start()
