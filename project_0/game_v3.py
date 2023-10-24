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


def score_game(random_predict) -> int:
    """За какое количество попыток в среднем за 10000 подходов угадывает наш алгоритм

    Args:
        random_predict ([type]): функция угадывания

    Returns:
        int: среднее количество попыток
    """
    count_ls = []
    #np.random.seed(1)  # Фиксируем сид для воспроизводимости
    random_array = np.random.randint(1, 101, size=(1000))  # Загадали список чисел

    for number in random_array:
        count_ls.append(random_predict(number))

    score = int(np.mean(count_ls))
    
    if str(score)[-1] == '1':
        print(f'Ваш алгоритм угадывает число в среднем за: {score} попытку')
    
    elif str(score)[-1] in ['2', '3', '4']:
        print(f'Ваш алгоритм угадывает число в среднем за: {score} попытки')
        
    else:
        print(f'Ваш алгоритм угадывает число в среднем за: {score} попыток')
        
    return(score)
    
    
score_game(best_game)