"""
Упрощенные тесты для приложения
"""

import unittest
import sys
import os

class TestBasicFunctionality(unittest.TestCase):
    """Тесты базовой функциональности"""
    
    def test_import_app(self):
        """Тест импорта приложения"""
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from app import app
        self.assertIsNotNone(app)
    
    def test_app_config(self):
        """Тест конфигурации приложения"""
        from app import app
        self.assertEqual(app.config['SECRET_KEY'], 'secret_key')
        self.assertIn('SQLALCHEMY_DATABASE_URI', app.config)
    
    def test_models_exist(self):
        """Тест существования моделей"""
        from app import Employee, Attendance
        self.assertIsNotNone(Employee)
        self.assertIsNotNone(Attendance)

class TestFlaskBasic(unittest.TestCase):
    """Базовые тесты Flask"""
    
    def setUp(self):
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from app import app
        app.config['TESTING'] = True
        self.client = app.test_client()
    
    def test_home_page(self):
        """Тест главной страницы"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_login_page_exists(self):
        """Тест, что страница логина существует"""
        response = self.client.get('/')
        # Проверяем что есть какой-то контент
        self.assertTrue(len(response.data) > 0)

def quick_test():
    """Быстрый тест для запуска вручную"""
    print("Быстрая проверка работы приложения...")
    
    try:
        # Импортируем
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from app import app
        
        print("[OK] Приложение импортировано")
        
        # Проверяем конфигурацию
        assert app.config['SECRET_KEY'] == 'secret_key'
        print("[OK] Конфигурация OK")
        
        # Проверяем модели
        from app import Employee, Attendance
        print("[OK] Модели импортированы")
        
        # Создаем тестового клиента
        with app.test_client() as client:
            response = client.get('/')
            assert response.status_code == 200
            print("[OK] Главная страница возвращает 200")
        
        print("\nВсе базовые проверки пройдены!")
        return True
        
    except Exception as e:
        print(f"[ERROR] Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("ЗАПУСК УПРОЩЕННЫХ ТЕСТОВ")
    print("=" * 60)
    
    # Сначала быстрый тест
    if not quick_test():
        print("\nБыстрый тест не прошел")
        exit(1)
    
    # Запускаем unittest
    print("\n" + "=" * 60)
    print("ЗАПУСК UNITTEST")
    print("=" * 60)
    
    unittest.main(verbosity=2)