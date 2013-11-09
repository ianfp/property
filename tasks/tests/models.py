from django.test import TestCase
from tasks.models import Supplier, Quote, Task, Property, Location, Asset,\
    Frequency, Priority
from datetime import date

class TaskTest(TestCase):
    def test_str(self):
        a = Asset(name = 'there ')
        t = Task(name = 'Hi', asset=a)
        self.assertEqual('Hi there', str(t))
        
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
            
    def test_frequency_object(self):
        """
        Ensure that the .frequency setter works with Frequency objects, too.
        """
        t = Task()
        for value in [0, 1, 6, 12]:
            t.frequency = Frequency(value)
            self.assertEqual(value, t._frequency)
        
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
        
        p = Property()
        p.save()
        l = Location(property = p)
        l.save()
        a = Asset(location = l)
        a.save()         
        t = Task(asset = a)
        t.name = 'Mop floors'
        t.frequency = 1
        t.save()
         
        q = Quote(supplier = s)
        q.amount = 4
        q.save()
        
        self.assertEqual(0, len(q.tasks.all()))
        
        q.tasks.add(t)
        self.assertEqual(1, len(q.tasks.all()))
          
        self.assertEqual
        self.assertEqual("$4.00 to Mop floors (Joe)", str(q))
        
        
class FrequencyTest(TestCase):
    def test_parse(self):
        tests = {
            ""    :  0,
            "  "  :  0,
            "1 m" :  1,
            "1M"  :  1,
            "2m"  :  2,
            "1 y" : 12,
            "3Y"  : 36
        }
        for string, value in tests.items():
            f = Frequency.parse(string)
            self.assertEqual(value, f.value)
            
            
class PriorityTest(TestCase):
    def test_parse(self):
        tests = {
            ""    :  Priority.MEDIUM,
            "  "  :  Priority.MEDIUM,
            "h"   :  Priority.HIGH,
            "high":  Priority.HIGH,
            "HI"  :  Priority.HIGH,
            "low" :  Priority.LOW,
            "L"   :  Priority.LOW,
        }
        for string, expected in tests.items():
            value = Priority.parse(string)
            self.assertEqual(expected, value)