import pygetwindow
from src.organizer.permissions.orgApp_close import org_app_close

all_windows = pygetwindow.getAllTitles()
print(all_windows)


process_names = ["Taskmgr.exe", "mmc.exe", "SystemSettings.exe"]
# # Список директорий / окон для закрытия (пишется title окна)
dir_names = ['*', '', 'orgApp Dev – t1.py', 'Как закрыть вкладку google crome '
                                        'при помощи python? - Google Chrome', 'Медиаплеер', 'Медиаплеер', '', 'Калькулятор', 'Калькулятор', 'NVIDIA GeForce Overlay', '', '', '', '', 'Microsoft Text Input Application', 'Program Manager']

org_app_close(process_names, dir_names)





