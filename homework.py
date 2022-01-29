# Модуль расчёта и отображения полной информации о тренировках
# по данным от блока датчиков.

from typing import ClassVar


# Базовый класс Training
class Training:
    """Базовый класс тренировки."""
    # Константа для перевода значений из метров в километры
    M_IN_KM: ClassVar[int] = 1000
    # Константа для перевода значений из часов в минуты
    MIN_IN_HOUR: ClassVar[int] = 60
    # Расстояние, которое спортсмен преодолевает за один шаг
    LEN_STEP: ClassVar[float] = 0.65

    def __init__(self,
                 # Количество совершённых действий
                 # (число шагов при ходьбе и беге либо гребков — при плавании)
                 action: int,
                 # Длительность тренировки
                 duration: float,
                 # Вес спортсмена
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    # Метод get_distance() возвращает дистанцию (в километрах),
    # которую преодолел пользователь за время тренировки
    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    # Метод get_mean_speed() возвращает значение
    # средней скорости движения во время тренировки
    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    # Метод get_spent_calories() возвращает число потраченных калорий
    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    # Метод show_training_info() возвращает объект класса сообщения
    def show_training_info(self) -> 'InfoMessage':
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_info = InfoMessage(type(self).__name__,
                                    self.duration,
                                    self.get_distance(),
                                    self.get_mean_speed(),
                                    self.get_spent_calories())
        return training_info


# Классы-наследники
# Класс беговой тренировки
class Running(Training):
    """Тренировка: бег."""
    # Свойства класса наследуются
    RUN_CONST_1: ClassVar[int] = 18
    RUN_CONST_2: ClassVar[int] = 20

    # Переопределенный метод get_spent_calories(),
    # возвращающий число потраченных калорий
    def get_spent_calories(self):
        spent_calories = ((self.RUN_CONST_1 * Training.get_mean_speed(self)
                          - self.RUN_CONST_2) * self.weight / Training.M_IN_KM
                          * self.duration * self.MIN_IN_HOUR)
        return spent_calories


# Класс спортивной ходьбы
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    WLK_COEFF_CALORIE_1: ClassVar[float] = 0.035
    WLK_COEFF_CALORIE_2: ClassVar[float] = 0.029

    def __init__(self,
                 # Основное считываемое действие во время тренировки - шаг
                 action: int,
                 # Длительность тренировки
                 duration: float,
                 # Вес спортсмена
                 weight: float,
                 # Рост спортсмена
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    # Переопределенный метод get_spent_calories(),
    # возвращающий число потраченных калорий
    def get_spent_calories(self) -> float:
        spent_calories = ((self.WLK_COEFF_CALORIE_1 * self.weight
                          + (Training.get_mean_speed(self) ** 2 // self.height)
                          * self.WLK_COEFF_CALORIE_2
                          * self.weight) * self.duration * self.MIN_IN_HOUR)
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    # Расстояние, которое спортсмен преодолевает за один гребок
    LEN_STEP: ClassVar[float] = 1.38

    def __init__(self,
                 # Количество гребков
                 action: int,
                 # Длительность тренировки
                 duration: float,
                 # Вес спортсмена
                 weight: float,
                 # Длина бассейна
                 length_pool: float,
                 # Количество проплытых бассейнов
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    # Метод возвращает значение средней скорости движения во время тренировки
    def get_mean_speed(self) -> float:
        mean_speed = (self.length_pool * self.count_pool
                      / Training.M_IN_KM / self.duration)
        return mean_speed

    # Переопределенный метод get_spent_calories(),
    # возвращающий число потраченных калорий
    def get_spent_calories(self) -> float:
        spent_calories = (self.get_mean_speed() + 1.1) * 2 * self.weight
        return spent_calories


# Класс для создания объектов сообщений
class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 # тип тренировки
                 training_type: str,
                 # длительность тренировки
                 duration: float,
                 # дистанция, преодолённая за тренировку
                 distance: float,
                 # средняя скорость движения
                 speed: int,
                 # килокалории потраченные за время тренировки
                 calories: int,
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    # Метод для вывода сообщений на экран
    def get_message(self) -> str:
        # Выводимое сообщение
        # все значения типа float округляются до 3 знаков после запятой
        return str(f'Тип тренировки: {self.training_type}; '
                   f'Длительность: {self.duration:.3f} ч.; '
                   f'Дистанция: {self.distance:.3f} км; '
                   f'Ср. скорость: {self.speed:.3f} км/ч; '
                   f'Потрачено ккал: {self.calories:.3f}.')


# Функция чтения принятых пакетов
def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    # Cловарь, в котором сопоставляются коды тренировок и классы
    training_type: dict = {'SWM': Swimming,
                           'RUN': Running,
                           'WLK': SportsWalking}
    return training_type.get(workout_type)(*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
