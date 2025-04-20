import math
from abc import ABC, abstractmethod
import unittest


#Абстрактный базовый класс для геометрических фигур
class Shape(ABC):
    n_dots = None

    def __init__(self):
        self.validate()
                 
    @abstractmethod
    def area(self) -> float:
        #Вычисление площади фигуры
        raise NotImplementedError("Метод area() не реализован")

    @abstractmethod
    def is_right_angled(self) -> bool:
        #проверка на то, является ли треугольник прямоугольным
        pass

    @abstractmethod
    def validate(self):
        raise NotImplementedError("Метод validate() не реализован")



class Circle(Shape):

    def __init__(self, radius: float):
        if radius < 0:
            raise ValueError("Ошибка, радиус не может быть отрицательным числом")
        self.radius = radius
    
    def area(self) -> float:
        s = math.pi * self.radius ** 2
        return s
    
    def is_right_angled(self) -> bool:
        return False
    
    def validate(self):
        return super().validate()

    

class Triangle(Shape):
    n_dots = 3 #количество точек 

    def __init__(self, a: float, b: float, c: float):
        sides = [a, b, c]
        if any(side <= 0 for side in sides):
            raise ValueError("Все стороны в треугольнике должны быть положительными числами")
        self.a = a
        self.b = b
        self.c = c

    #пример решения без использования библиотеки math
    def area(self) -> float:
        #формула Герона
        p = (self.a + self.b + self.c) / 2
        s = (p * (p - self.a) * (p - self.b) * (p - self.c)) ** 0.5
        return s
    
    def is_right_angled(self) -> bool:
        #Теорема Пифагора
        sides = [self.a, self.b, self.c]
        sides.sort()
        c = math.isclose(sides[0] ** 2 + sides[1] ** 2, sides[2] ** 2, rel_tol=1e-9)    
        return c
    
    def validate(self):
        #проверка на неравенство: каждая сторона меньше суммы двух других
        if not (self.a + self.b > self.c and 
                self.a + self.c > self.b and 
                self.b + self.c > self.a): # если меньше выдаёт ошибку
            raise ValueError("Неравенство треугольника не выполнено")
        return (self.a, self.b, self.c)



class Rectangle(Shape):
    n_dots = 4

    def __init__(self, a: float, b: float):
        self.a = a
        self.b = b

    def area(self):
        s = self.a * self.b
        return s
    
    def is_right_angled(self) -> bool:
        return True
    
    def validate(self):
        return super().validate()

#Функция вычисления площади фигуры без знания её типа в compile-time
def calc_area(shape: Shape):
    return shape.area()



#Юнит тесты для проверки функциональности


class TestShapes(unittest.TestCase):
    
    def test_circle(self):
        #radius = float(input("Введите радиус круга: "))
        circle = Circle(5)
        self.assertAlmostEqual(circle.area(), math.pi * 5 ** 2, places = 5)
        
    def test_triangle(self):
        triange = Triangle(3, 4, 5)
        self.assertAlmostEqual(triange.area(), 6.0)
        self.assertTrue(triange.is_right_angled())

        triange_2 = Triangle(5, 5, 5)
        self.assertAlmostEqual(triange_2.area(), 10.83, places = 2)
        self.assertFalse(triange_2.is_right_angled())

    def test_rectangle(self):
        rectangle = Rectangle(4, 5)
        self.assertAlmostEqual(rectangle.area(), 20.0)

        
    def test_calc_area(self):
        shapes = [Circle(5), Triangle(3, 4, 5), Rectangle(3, 4)]
        areas = [calc_area(shape) for shape in shapes]
        self.assertAlmostEqual(areas[0], math.pi * 25, places = 2)
        self.assertAlmostEqual(areas[1], 6.0, places = 2)
        self.assertAlmostEqual(areas[2], 12.0, places = 2)




if __name__ == "__main__":
    unittest.main()



