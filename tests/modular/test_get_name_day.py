import unittest
from datetime import datetime
from src.organizer.get_name_day import get_name_day

class TestGetNameDay(unittest.TestCase):

    def test_get_name_day_today(self):
        # Получить имя для сегодняшней даты
        expected_date = datetime.now().strftime('Day_%d_%m_%a')
        self.assertEqual(get_name_day(), expected_date)

    def test_get_name_day_custom_date(self):
        # Получить имя для определенной даты
        custom_date = '12.05.2024'
        expected_date = datetime.strptime(custom_date, '%d.%m.%Y').strftime('Day_%d_%m_%a')
        self.assertEqual(get_name_day(custom_date), expected_date)

    def test_get_name_day_invalid_date_format(self):
        # Проверить обработку недопустимого формата даты
        invalid_date = '2024-05-12'
        with self.assertRaises(ValueError):
            get_name_day(invalid_date)

if __name__ == '__main__':
    unittest.main()
