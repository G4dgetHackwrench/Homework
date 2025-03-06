import numpy as np


def best_game(number: int = 1) -> int:
    """Сначала устанавливаем число равное среднему значению разброса чисел, а потом изменяем интервал поиска
       в зависимости от того, число больше или меньше нужного.
       Функция принимает загаданное число и возвращает число попыток
       
    Args:
        number (int, optional): Загаданное число. Defaults to 1.

    Returns:
        int: Число попыток
    """
    count = 0
    min_num = 0    # Инициализируем переменную для нижней границы поиска
    max_num = 100    # Инициализируем переменную для верхней границы поиска
    predict = np.round((min_num + max_num) /2)
    
    while number != predict:
        count += 1
        if number > predict:
            min_num = predict    # Увеличиваем нижнюю границу интервала поиска
            predict = np.round((min_num + max_num) /2)
            
        elif number < predict:
            max_num = predict    # Уменьшаем верхнюю границу интервала поиска
            predict = np.round((min_num + max_num) /2)

    return count