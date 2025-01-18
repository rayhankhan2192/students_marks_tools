from django.db import models

class Batch(models.Model):
    batch_name = models.CharField(max_length=50, blank=False, null=False)
    section = models.CharField(max_length=50, blank=False, null=False)
    course_name = models.CharField(max_length=50, blank=False, null=False)
    course_code = models.CharField(max_length=50, blank=False, null=False) 
    
    class Meta:
        verbose_name = "Batch"
        verbose_name_plural = "Batch"

    def __str__(self):
        return f"{self.batch_name} ({self.section})"


class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True, null=False)
    marks = models.DecimalField(max_digits=5, decimal_places=2, default=0, blank=True, null=True)
    section = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='students')
    
    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Student"

    def __str__(self):
        return f"{self.student_id}"
