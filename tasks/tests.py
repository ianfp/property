from django.test import TestCase
from tasks.models import Supplier, Quote, Task
from datetime import date

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
            
    def test_next_due(self):
        t = Task()
        t.last_done = date(2012, 1, 1)
        t.frequency = 1
        
        self.assertEqual(date(2012, 2, 1), t.next_due)
        
    def test_next_due_null(self):
        t = Task()
        t.last_done = None
        t.frequency = 1
        
        self.assertIsNone(t.next_due)
        
    def test_next_due_zero(self):
        t = Task()
        t.last_done = date(2012, 1, 1)
        t.frequency = 0
        
        self.assertIsNone(t.next_due)
                

class SupplierTest(TestCase):
    def test_str(self):
        s = Supplier()
        s.name = 'Joe'
        self.assertEqual("Joe", str(s))

class QuoteTest(TestCase):
    def test_tasks(self):
        s = Supplier()
        s.name = 'Joe'
        s.save()
         
        t = Task()
        t.description = 'Mop floors'
        t.frequency = 1
        t.save()
         
        q = Quote()
        q.supplier = s
        q.amount = 4
        q.save()
        
        self.assertEqual(0, len(q.tasks.all()))
        
        q.tasks.add(t)
        self.assertEqual(1, len(q.tasks.all()))
          
        self.assertEqual
        self.assertEqual("$4.00 to Mop floors (Joe)", str(q))
        
        
         