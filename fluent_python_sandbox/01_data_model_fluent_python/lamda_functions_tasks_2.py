import collections
from functools import reduce

logss = [
  "2025-05-01 10:15:23 ERROR Failed to connect to DB",
  "2025-05-01 10:16:01 WARN Slow query (2.3s)",
  "2025-05-01 10:17:45 INFO User login success",
  "2025-05-01 10:18:12 ERROR Timeout on API call",
  "2025-05-01 10:19:30 WARN High memory usage 85%",
  "2025-05-01 10:20:00 ERROR Disk full",
]
'''
Задание 5 (логи)
# 1. filter: Оставить только строки с уровнем ERROR
# 2. map: Из каждой ERROR-строки извлечь сообщение (всё после уровня)
# 3. reduce: Соединить все сообщения об ошибках в одну строку через "; "
# 4. sorted: Отсортировать исходные логи (все) по времени от старых к новым
#    (подсказка: key=lambda x: x[:19])
# 5. match/case: Для каждой строки лога:
#    - Если уровень ERROR → вывести "[!] {message}"
#    - Если уровень WARN → вывести "[?] {message}"
#    - Если уровень INFO → вывести "[i] {message}"
#    - Если другой уровень → "[?] Unknown level: {level}"
'''
def task1():
  error_level1= list(filter(lambda s: s.count('ERROR')>0, logss))
  error_level2=[s for s in logss if s.count('ERROR')>0]
  error_level3=[s for s in logss if s.find('ERROR')!=-1]
  print(error_level3)
  err_message=list(map(lambda t: t.split(maxsplit=3)[3], error_level1))
  print(err_message)
  print('; '.join(err_message))
  conc_str=reduce(lambda acc, s: acc+'; ' + s, err_message)
  print(conc_str)
  sorted_str=sorted(logss, key=lambda x: x[:19])
  print(sorted_str)
  for s in logss:
    parts= s.split(maxsplit=3)
    match parts:
      case [data, time, 'ERROR', message]:
        print(f'[!] {message}')
      case[data, time, 'WARN', message]:
        print(f'[?] {message}')
      case[data, time, 'INFO', message]:
        print(f'[i] {message}')

# ========== Данные: студенты и их оценки ==========
students = [
  {"name": "Alice", "grades": [85, 92, 78, 90], "status": "active"},
  {"name": "Bob", "grades": [45, 55, 60, 48], "status": "active"},
  {"name": "Charlie", "grades": [95, 98, 100, 92], "status": "inactive"},
  {"name": "Diana", "grades": [65, 70, 72, 68], "status": "active"},
  {"name": "Eve", "grades": [88, 79, 84, 91], "status": "active"},
  {"name": "Frank", "grades": [30, 40, 35, 25], "status": "inactive"},
]
# ========== Задача 6 (студенты и успеваемость) ==========
# 1. filter: Оставить только активных студентов
# 2. map: Для каждого активного студента вычислить средний балл
# 3. reduce: Найти общий средний балл среди всех активных студентов
# 4. sorted: Отсортировать всех студентов (активных и неактивных) по имени (по алфавиту)
# 5. match/case: Для каждого студента вывести информацию:
#    - Если статус не "active" → "❌ {name} is inactive"
#    - Если средний балл >= 90 → "🏆 {name}: {avg:.1f} (excellent)"
#    - Если средний балл >= 60 → "✅ {name}: {avg:.1f} (good)"
#    - Если средний балл < 60 → "⚠️ {name}: {avg:.1f} (need support)"
#    (Подсказка: вы можете вычислить средний балл прямо в case, используя гвард и sum(grades)/len(grades))

def task2():
  active_students = list(filter(lambda student: student['status']== 'active', students))
  print(active_students)
  grade_mean_map = list(map(lambda x: sum(x['grades'])/len(x['grades']), active_students))
  grade_mean_compreh = [f'{student['name']}:{sum(student['grades'])/len(student['grades'])}' for student in active_students]
  grade_mean_reduce = [f'{student['name']}_{reduce(lambda acc, x: acc + x, student['grades'], 0)/len(student['grades'])}' for student in active_students]
  print(grade_mean_map)
  print(grade_mean_compreh)
  print(grade_mean_reduce)
  sorted_by_name = [s['name'] for s in sorted(students, key=lambda student: student['name'], reverse=False)]
  print(sorted_by_name)
  for student in students:
    mean_grades=sum(student['grades'])/len(student['grades'])
    match student:
      case{'name':name, 'status':status} if status != 'active':
        print(f'❌ {name} is inactive')
      case{'name':name} if mean_grades >=85:
        print(f'🏆 {name}: {mean_grades:.1f} (best of the best)')
      case{'name':name} if mean_grades >=65 and mean_grades<85:
        print(f'✅ {name} : {mean_grades:.1f} (good student)')
      case{'name':name} if mean_grades <65:
        print(f'⚠️ {name} need support')

if __name__ == '__main__':
    # task1()
    task2()