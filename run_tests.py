#!/usr/bin/env python3
"""
Упрощенный скрипт для запуска тестов
"""

import sys
import os
import subprocess

def run_simple_tests():
    """Запускает простые тесты"""
    print("=" * 60)
    print("ЗАПУСК ПРОСТЫХ ТЕСТОВ")
    print("=" * 60)
    
    try:
        # Запускаем простые тесты
        result = subprocess.run(
            [sys.executable, 'test_simple.py'],
            capture_output=True,
            text=True,
            encoding='utf-8'  # Явно указываем кодировку
        )
        
        print(result.stdout)
        
        if result.returncode == 0:
            print("[OK] Простые тесты прошли успешно!")
            return True
        else:
            print("[ERROR] Простые тесты не прошли")
            if result.stderr:
                print("\nОшибки:")
                print(result.stderr)
            return False
    
    except Exception as e:
        print(f"[ERROR] Ошибка при запуске простых тестов: {e}")
        return False

def run_unittest():
    """Запускает unittest тесты"""
    print("\n" + "=" * 60)
    print("ЗАПУСК UNITTEST ТЕСТОВ")
    print("=" * 60)
    
    try:
        # Запускаем только базовые тесты
        result = subprocess.run(
            [sys.executable, '-m', 'unittest', 'test_app.TestBasicFunctionality', '-v'],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        print(result.stdout)
        
        if result.returncode == 0:
            print("\n[OK] Базовые unittest тесты прошли успешно!")
            return True
        else:
            print("\n[ERROR] Базовые unittest тесты не прошли")
            if result.stderr:
                print("Ошибки:")
                print(result.stderr)
            return False
            
    except Exception as e:
        print(f"[ERROR] Ошибка при запуске unittest: {e}")
        return False

def check_project_structure():
    """Проверяет структуру проекта"""
    print("\n" + "=" * 60)
    print("ПРОВЕРКА СТРУКТУРЫ ПРОЕКТА")
    print("=" * 60)
    
    required_files = [
        ('app.py', True),
        ('requirements.txt', True),
        ('templates/login.html', False),
        ('templates/dashboard.html', False),
        ('templates/add_employee.html', False),
        ('static/style.css', False),
        ('test_simple.py', True),
        ('test_app.py', True),
    ]
    
    all_exist = True
    for file_path, required in required_files:
        exists = os.path.exists(file_path)
        
        if required and not exists:
            all_exist = False
            print(f"{file_path:30} [ERROR] ОТСУТСТВУЕТ (ОБЯЗАТЕЛЬНЫЙ)")
        elif exists:
            print(f"{file_path:30} [OK] СУЩЕСТВУЕТ")
        else:
            print(f"{file_path:30} [WARN] ОТСУТСТВУЕТ")
    
    return all_exist

def run_flask_basic_test():
    """Запускает базовый тест Flask"""
    print("\n" + "=" * 60)
    print("БАЗОВЫЙ ТЕСТ FLASK")
    print("=" * 60)
    
    try:
        # Импортируем и тестируем
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from app import app
        
        with app.test_client() as client:
            # Тестируем главную страницу
            response = client.get('/')
            print(f"Главная страница: HTTP {response.status_code}")
            
            if response.status_code == 200:
                print("[OK] Главная страница работает")
                return True
            else:
                print("[WARN] Главная страница не вернула 200")
                return False
                
    except Exception as e:
        print(f"[ERROR] Ошибка Flask теста: {e}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("ТЕСТИРОВАНИЕ СИСТЕМЫ УЧЕТА РАБОЧЕГО ВРЕМЕНИ")
    print("=" * 60)
    
    # 1. Проверяем структуру
    structure_ok = check_project_structure()
    if not structure_ok:
        print("\n[ERROR] Неправильная структура проекта!")
        sys.exit(1)
    
    # 2. Запускаем простые тесты
    simple_tests_ok = run_simple_tests()
    
    if not simple_tests_ok:
        print("\n[ERROR] Простые тесты не прошли!")
        sys.exit(1)
    
    # 3. Запускаем Flask тест
    flask_test_ok = run_flask_basic_test()
    
    # 4. Запускаем unittest тесты
    unittest_ok = run_unittest()
    
    print("\n" + "=" * 60)
    print("ИТОГИ ТЕСТИРОВАНИЯ")
    print("=" * 60)
    
    print(f"Структура проекта: {'[OK]' if structure_ok else '[ERROR]'}")
    print(f"Простые тесты: {'[OK]' if simple_tests_ok else '[ERROR]'}")
    print(f"Flask тест: {'[OK]' if flask_test_ok else '[ERROR]'}")
    print(f"Unittest тесты: {'[OK]' if unittest_ok else '[ERROR]'}")
    
    if structure_ok and simple_tests_ok and flask_test_ok and unittest_ok:
        print("\nВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        sys.exit(0)
    else:
        print("\nЕСТЬ НЕПРОЙДЕННЫЕ ТЕСТЫ")
        sys.exit(1)