from dataclasses import dataclass, asdict
from typing import Sequence, Dict, Tuple, List, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    message: str = ('Тип тренировки: {training_type}; '
                    'Длительность: {duration:.3f} ч.; '
                    'Дистанция: {distance:.3f} км; '
                    'Ср. скорость: {speed:.3f} км/ч; '
                    'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.message.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    MIN_IN_HOUR: int = 60
    LEN_STEP: float = 0.65
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Определить get_spent_calories')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            training_type=self.__class__.__name__,
            duration=self.duration,
            distance=self.get_distance(),
            speed=self.get_mean_speed(),
            calories=self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""
    RUN_COEFF_1: float = 18
    RUN_COEFF_2: float = 20

    def get_spent_calories(self) -> float:
        speed_and_coeff = (self.RUN_COEFF_1 * self.get_mean_speed()
                           - self.RUN_COEFF_2) * self.weight
        duration_in_minutes = self.duration * self.MIN_IN_HOUR

        return speed_and_coeff / self.M_IN_KM * duration_in_minutes


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    WLK_COEFF_1: float = 0.035
    WLK_COEFF_2: float = 0.029

    def __init__(self,
                 action,
                 duration,
                 weight,
                 height
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        weight_and_coeff_1 = self.WLK_COEFF_1 * self.weight
        weight_and_coeff_2 = self.WLK_COEFF_2 * self.weight
        mean_speed_and_weight = ((self.get_mean_speed() ** 2)
                                 // self.height)
        duration_in_minutes = self.duration * self.MIN_IN_HOUR

        return (weight_and_coeff_1 + mean_speed_and_weight
                * weight_and_coeff_2) * duration_in_minutes


class Swimming(Training):
    """Тренировка: плавание."""

    SWM_COEFF_1: float = 1.1
    SWM_COEFF_2: float = 2
    LEN_STEP: float = 1.38

    def __init__(self,
                 action,
                 duration,
                 weight,
                 length_pool,
                 count_pool
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Расчитать расстояние в бассейне."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Расчитать среднюю скорость в бассейне."""
        distance_in_meters = self.length_pool * self.count_pool
        distance_in_km = distance_in_meters / self.M_IN_KM

        return distance_in_km / self.duration

    def get_spent_calories(self) -> float:
        mean_speed_and_coeff = self.get_mean_speed() + self.SWM_COEFF_1

        return mean_speed_and_coeff * self.SWM_COEFF_2 * self.weight


def read_package(workout_type: str, data: Sequence[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    title_of_the_workout = Dict[str, Type[Training]]

    training_name: title_of_the_workout = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in training_name:
        raise NotImplementedError('Возможно выкинуть исключение')

    return training_name[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: Sequence[Tuple[str, List[int]]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)