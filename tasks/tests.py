from django.test import TestCase
from tasks.models import Supplier, Estimate, Task


class TaskTest(TestCase):
    def test_str(self):
        t = Task()
        t.description = 'Hi'
        self.assertEqual('Hi', str(t))
        
    def test_frequency(self):
        t = Task()
        tests = {
             0: "once",
             1: "every month",
             2: "every 2 months",
             12: "every year",
             13: "every 13 months",
             24: "every 2 years"
        }
        
        for value, expected in tests.items():
            t.frequency = value
            self.assertEqual(expected, str(t.frequency))
                

class SupplierTest(TestCase):
    def test_str(self):
        s = Supplier()
        s.name = 'Joe'
        self.assertEqual("Joe", str(s))

class EstimateTest(TestCase):
    def test_tasks(self):
        s = Supplier()
        s.name = 'Joe'
        s.save()
         
        t = Task()
        t.description = 'Mop floors'
        t.frequency = 1
        t.save()
         
        e = Estimate()
        e.supplier = s
        e.amount = 4
        e.save()
        
        self.assertEqual(0, len(e.tasks.all()))
        
        e.tasks.add(t)
        self.assertEqual(1, len(e.tasks.all()))
          
        self.assertEqual
        self.assertEqual("$4.00 to Mop floors (Joe)", str(e))
        
        
         