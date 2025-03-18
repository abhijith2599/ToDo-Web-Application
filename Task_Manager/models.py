from django.db import models
from django.contrib.auth.models import User

from django.utils.timezone import now

# Create your models here.

class TaskModel(models.Model):

    Task_Name = models.CharField(max_length=100)

    Task_Description = models.TextField(max_length=100)

    Created_Date = models.DateTimeField(auto_now=True)

    Due_Date = models.DateTimeField()

    Priority_Level = [
                        ('Low','Low'),
                        ('Medium','Medium'),
                        ('High','High')
                    ]

    Priority = models.CharField(max_length=100,choices=Priority_Level)      # here choices is given as a list before , if we want  we can add it here

    Points = models.IntegerField(default=0)

    Status = models.BooleanField(default=False)

    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):         # This is called string representation , to show an object with it's Name 
        
        return self.Task_Name
    
    def complete(self):

        if self.Status == False:

            if now() < self.Due_Date:

                self.Points += 5
            
            self.Status = True
            self.save()