from abc import ABC, abstractmethod
class Absclass(ABC):
    def print(self, x):
        print("Pasesed VALUUUUUUUUU: ", x)
    @abstractmethod
    def task(self):
        print("We are inside  ABUCKLASUUUUUUUUUUUU task")
class test_class(Absclass):
    def task(self):
        print("WE ARE INSIDOO TESTO_CLASOOOOOOOOOOOOOO task")
test_obj = test_class()
test_obj.task()
test_obj.print(100)