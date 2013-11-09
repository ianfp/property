from datetime import date
from django.db import models
from django.core.validators import MaxValueValidator
from dateutil.relativedelta import relativedelta
import re


class Property(models.Model):
    """
    Any building or other kind of property owned by the organization.
    """
    name = models.CharField(max_length=255)
    
    class Meta:
        verbose_name_plural = "properties"
    
    def __str__(self):
        return self.name
    

class Location(models.Model):
    """
    A room or subdivision of a property in which Assets are located.
    """
    name = models.CharField(max_length=255)
    property = models.ForeignKey(Property)
    
    def __str__(self):
        return self.name
    
    
class Asset(models.Model):
    """
    An asset owned by the organization that has value or needs
    maintenance.
    """
    name = models.CharField(max_length=255)
    location = models.ForeignKey(Location)
    quantity = models.IntegerField(default=1)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Frequency(object):
    """
    Describes how often a task must take place.
    """
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
        
    @classmethod
    def parse(cls, string):
        """
        Factory method.
        @rtype: Frequency
        """
        string = string.strip()
        if string == '':
            return cls(0)
        match = re.search('(\d+)\s*([YyMm])', string)
        if match:
            base = int(match.group(1))
            multiplier = cls._parse_multiplier(match.group(2))
            return cls(base * multiplier)
        else:
            raise RuntimeError("Invalid frequency {}".format(string))
            
    @classmethod
    def _parse_multiplier(cls, string):
        """
        @type string: str
        """
        string = string.lower()
        if string == 'y':
            return 12
        elif string == 'm':
            return 1
        else:
            raise RuntimeError("Invalid multiplier {}".format(string))
    
    
class Priority(object):
    """
    The priority of a task.
    """
    HIGH = 5
    MEDIUM = 0
    LOW = -5
    
    MAP = (
        (HIGH, 'high'),
        (MEDIUM, 'medium'),
        (LOW, 'low'),
    )
    
    @classmethod
    def parse(cls, string):
        """
        @type string: str
        @rtype: int
        """
        string = str(string).strip().lower()
        if not string:
            return cls.MEDIUM

        for value, label in cls.MAP:
            if string[0] == label[0]:
                return value
        return cls.MEDIUM
        

class Task(models.Model):
    """
    One-time or recurring work that needs to be done to maintain an
    Asset.
    """
    name = models.CharField(max_length=255)
    asset = models.ForeignKey(Asset)
    details = models.TextField(blank=True)
    _frequency = models.IntegerField(default=0, db_column="frequency")
    last_done = models.DateField(blank=True, null=True,
        validators=[MaxValueValidator(date.today())])
    priority = models.IntegerField(choices=Priority.MAP, default=0)
    estimate = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
                
    def __str__(self):
        return "{} {}".format(self.name, self.asset).strip()
    
    @property
    def frequency(self):
        return Frequency(self._frequency)
    
    @frequency.setter
    def frequency(self, freq):
        if type(freq) is Frequency:
            freq = freq.value
        self._frequency = freq
        
    @property
    def next_due(self):
        if self.last_done is None:
            return None
        elif self._frequency == 0:
            return None
        return self.last_done + relativedelta(months=self._frequency)
    
    @property
    def location(self):
        return self.asset.location


class Contact(models.Model):
    """
    A person's contact info.
    """
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True)
    telephone = models.CharField(max_length=25, blank=True)
    email = models.EmailField(blank=True)
    
    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name).strip()
        
    
class Supplier(models.Model):
    """
    A person or company that does tasks.
    """
    name = models.CharField(max_length=50)
    website = models.URLField(blank=True)
    telephone = models.CharField(max_length=25, blank=True)
    contacts = models.ManyToManyField(Contact, blank=True)
    
    def __str__(self):
        return self.name
    

class Quote(models.Model):
    """
    The amount a Supplier will charge to do one or more Tasks.
    """
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
 
