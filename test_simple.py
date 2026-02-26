"""
Простые тесты для проверки базовой функциональности
"""

import sys
import os

def test_imports():
    """Тест импортов"""
    try:
        # Импортируем напрямую из app.py
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        # Импортируем приложение
        from app import app, db, Employee, Attendance
        
        print("  [OK] Все импорты работают корректно")
        return True
    except ImportError as e:
        print(f"  [ERROR] Ошибка импорта: {e}")
        return False
    except Exception as e:
        print(f"  [ERROR] Другая ошибка: {e}")
        return False

def test_app_config():
    """Тест конфигурации приложения"""
    try:
        from app import app
        
        # Проверяем конфигурацию
        assert app.config['SECRET_KEY'] == 'secret_key'
        assert 'SQLALCHEMY_DATABASE_URI' in app.config
        
        print("  [OK] Конфигурация приложения корректна")
        return True
    except Exception as e:
        print(f"  [ERROR] Ошибка конфигурации: {e}")
        return False

def test_database_models():
    """Тест моделей базы данных"""
    try:
        from app import Employee, Attendance
        from datetime import date, datetime
        
        print("  [OK] Модели Employee и Attendance доступны")
        
        # Проверяем наличие атрибутов у Employee
        emp = Employee(name="Тест", position="Тест", hire_date=date.today())
        assert hasattr(emp, 'id')
        assert hasattr(emp, 'name')
        assert hasattr(emp, 'position')
        assert hasattr(emp, 'hire_date')
        
        # Проверяем наличие атрибутов у Attendance
        att = Attendance(employee_id=1, date=date.today(), check_in=datetime.now())
        assert hasattr(att, 'id')
        assert hasattr(att, 'employee_id')
        assert hasattr(att, 'date')
        assert hasattr(att, 'check_in')
        assert hasattr(att, 'check_out')
        
        print("  [OK] Модели имеют все необходимые атрибуты")
        return True
    except Exception as e:
        print(f"  [ERROR] Ошибка при тесте моделей: {e}")
        return False

def test_flask_routes_simple():
    """Упрощенный тест Flask маршрутов"""
    try:
        from app import app
        
        # Создаем тестового клиента
        with app.test_client() as client:
            print("  [OK] Flask test client создан")
            
            # Главная страница должна возвращать 200
            response = client.get('/')
            if response.status_code == 200:
                print("  [OK] Главная страница возвращает 200 OK")
                return True
            else:
                print(f"  [WARN] Главная страница вернула {response.status_code}")
                return False
    except Exception as e:
        print(f"  [ERROR] Ошибка при тесте маршрутов: {e}")
        return False

def test_app_creation():
    """Тест создания приложения"""
    try:
        from app import app
        # Проверяем, что приложение было создано
        assert app is not None
        print("  [OK] Приложение успешно создано")
        return True
    except Exception as e:
        print(f"  [ERROR] Ошибка создания приложения: {e}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("ЗАПУСК ПРОСТЫХ ТЕСТОВ")
    print("=" * 60)
    
    tests = [
        ("Создание приложения", test_app_creation),
        ("Импорты", test_imports),
        ("Конфигурация", test_app_config),
        ("Модели БД", test_database_models),
        ("Маршруты Flask", test_flask_routes_simple),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\nТест: {test_name}")
        result = test_func()
        results.append(result)
    
    print("\n" + "=" * 60)
    print("РЕЗУЛЬТАТЫ:")
    print("=" * 60)
    
    all_passed = all(results)
    for i, (test_name, _) in enumerate(tests):
        status = "[OK]" if results[i] else "[ERROR]"
        print(f"{test_name}: {status}")
    
    if all_passed:
        print("\nВСЕ ПРОСТЫЕ ТЕСТЫ ПРОШЛИ УСПЕШНО!")
        sys.exit(0)
    else:
        print("\nНЕКОТОРЫЕ ТЕСТЫ НЕ ПРОШЛИ")
        sys.exit(1)