from csv import DictReader
from tasks.models import Location, Asset, Task, Frequency, Priority
from datetime import datetime

def import_csv(prop, upload):
    """
    Imports a csv file of tasks and assets into the given prop.
    @type prop: Property
    @type upload: UploadedFile
    """
    csv = DictReader(upload)
    location = None
    asset = None
    for row in csv:
        location = _get_location(row, location, prop)
        asset = _get_asset(row, asset, location)
        if row['task'] == '':
            continue
        _create_task(row, asset)
        
     
def _get_location(row, current, prop):
    if row['location'] == '':
        if current is None:
            raise RuntimeError("Invalid CSV file")
        return current
    try:
        location = Location.objects.get(
            property__pk=prop.pk,
            name__iexact=row['location'])
    except Location.DoesNotExist:
        location = Location(name=row['location'], property=prop)
        location.save()
    return location

def _get_asset(row, current, location):
    if row['asset'] == '':
        if current is None:
            raise RuntimeError("Invalid CSV file")
        return current
    try:
        asset = Asset.objects.get(
            location__pk=location.pk,
            name__iexact=row['asset'])
    except Asset.DoesNotExist:
        asset = Asset(
            name=row['asset'],
            location=location)
    if row['quantity'] != '':
        asset.quantity = int(row['quantity'])
    asset.save()
    return asset

def _create_task(row, asset):
    try:
        task = Task.objects.get(
            asset__pk=asset.pk,
            name__iexact=row['task'])
    except Task.DoesNotExist:
        task = Task(name=row['task'], asset=asset)
    task.frequency = Frequency.parse(row['frequency'])
    task.last_done = _parse_last_done(row['last done'])
    task.priority = Priority.parse(row['priority'])
    if row['estimate'] != '':
        task.estimate = float(row['estimate'])
    task.save()
    return task
    
    
def _parse_last_done(string):
    formats = ['%Y', '%Y-%m', '%Y-%m-%d']
    for fmt in formats:
        try:
            return datetime.strptime(string, fmt).date()
        except ValueError:
            pass
    return None
