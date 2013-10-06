from django.db import models

class Task(models.Model):
    PRIORITIES = (
        ( 5, 'High'),
        ( 0, 'Medium'),
        (-5, 'Low'),
    )
    description = models.CharField(max_length=255)
    details = models.TextField(blank=True)
    _frequency = models.IntegerField(default=0, db_column="frequency")
    priority = models.IntegerField(choices=PRIORITIES, default=0)
    
    class Frequency(object):
        def __init__(self, value):
            self.value = value
            
        def __str__(self):
            num = self.value
            unit = "month"
            if num % 12 == 0:
                num = int(num / 12)
                unit = "year"
            if num == 0:
                return "once"
            elif num == 1:
                return "every {}".format(unit)
            else:
                return "every {} {}s".format(num, unit)
                
    def __str__(self):
        return self.description
    
    @property
    def frequency(self):
        return self.Frequency(self._frequency)
    
    @frequency.setter
    def frequency(self, integer):
        self._frequency = integer


class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True)
    telephone = models.CharField(max_length=25, blank=True)
    email = models.EmailField(blank=True)
    
    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name).strip()
        
    
class Supplier(models.Model):
    name = models.CharField(max_length=50)
    website = models.URLField(blank=True)
    telephone = models.CharField(max_length=25, blank=True)
    contacts = models.ManyToManyField(Contact, blank=True)
    
    def __str__(self):
        return self.name
    

class Estimate(models.Model):
    supplier = models.ForeignKey(Supplier)
    tasks = models.ManyToManyField(Task)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return "${:.2f} to {} ({})".format(self.amount, self._summarize_tasks(), self.supplier)
    
    def _summarize_tasks(self):
        summary = ", ".join([str(task) for task in self.tasks.all()])
        if len(summary) > 40:
            summary = summary[:37] + '...'
        return summary
 
    
