#!/usr/bin/env python3
"""
Минимальный тест для проверки работы
"""

print("=" * 50)
print("МИНИМАЛЬНЫЙ ТЕСТ ПРИЛОЖЕНИЯ")
print("=" * 50)

try:
    # 1. Импортируем приложение
    from app import app
    print("[OK] Шаг 1: Приложение импортировано")
    
    # 2. Проверяем конфигурацию
    print(f"[OK] Шаг 2: Секретный ключ = {app.config['SECRET_KEY']}")
    
    # 3. Проверяем модели
    from app import Employee, Attendance
    print("[OK] Шаг 3: Модели импортированы")
    
    # 4. Создаем тестового клиента
    with app.test_client() as client:
        print("[OK] Шаг 4: Тестовый клиент создан")
        
        # 5. Тестируем главную страницу
        response = client.get('/')
        print(f"[OK] Шаг 5: Главная страница - HTTP {response.status_code}")
        
        if response.status_code == 200:
            print("\nВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        else:
            print(f"\n[WARN] Главная страница вернула {response.status_code} вместо 200")
    
except Exception as e:
    print(f"\n[ERROR] ОШИБКА: {e}")
    import traceback
    traceback.print_exc()
    exit(1)