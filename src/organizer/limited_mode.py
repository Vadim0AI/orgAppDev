from src.db_querys.get.extract_db import extract_db
from src.organizer.links import path_to_db
from datetime import date


class LimitedMode:
    """ 
    self.status может принимать следующие значения:
    1. 'indefinite' - неопределенное значение;
    2. 'only shedule' - расписания на сегодня нет - можно только составлять расписание;
    3. 'no leisure' - расписание не было составлено заранее на сегодня, его составили сегодня же. Поэтому запрещено добавлять развлекательные РБ и другие подобные.
    4. 'no limited' - никаких ограничений на добавление РБ. Расписание на сегодня было составлено заранее, как минимуум еще вчера.
    """

    def __init__(self):
        self.status: str = 'indefinite'


    def get_status(self, date_for_query: str = 'today'):
        """ Возвращает статус limited_status на основе БД days 
        
        date_for_query (str) - дата по которой мы возьмем расписания и проверим статус limited_status.

        Алгоритм работы: 
        Обратиться к БД и получить список кортежей day за сегодня по значению limited_status, превратить его просто в список. Если в этом списке есть 'no limited' - то соответственно такой и статус, также и с 'no leisure', если ничего из этого нет, а есть только 'indefinite' или 'only shedule' - то 'only shedule'.

        Returns:
        limited_status (str) - статус режима ограниченной функциональности см. db_install.
        
        """

        if date_for_query == 'today':
            # Получение сегодняшней даты
            date_for_query = date.today()
            # Форматирование даты в dd.mm.yy
            date_for_query = date.strftime("%d.%m.%y")

        # Поучаем из БД
        where_query = f'date = {date}'
        status_lst_one: list = extract_db(select_column='limited_status', path_db=path_to_db, table_name='days', where_condition=where_query)
        # Превращаем список кортежей в список
        status_lst_two: list = []
        for tpl in status_lst_one:
            status_lst_two.append(tpl[0])
        # Выполняем проверки и выводим результат
        if 'no limited' in status_lst_two:
            self.status = 'no limited'
            return 'no limited'
        elif 'no leisure' in status_lst_two:
            self.status = 'no leisure'
            return 'no leisure'
        else:
            self.status = 'only shedule'
            return 'only shedule'


    def set_status(self):
        # Обращаемся к БД days и записываем в limited_status указанный в параметрах статус для последнего расписания на день
        pass


