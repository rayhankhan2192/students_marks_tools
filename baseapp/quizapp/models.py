from django.db import models

class Batch(models.Model):
     batch_name = models.CharField(max_length=100)

     def __str__(self):
        return self.batch_name

class Section(models.Model):
     section_name = models.CharField(max_length=100)
     batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='sections')

     def __str__(self):
        return f"{self.section_name} ({self.batch.batch_name})"

class Quizs(models.Model):
     title = models.CharField(max_length=100)
     section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='quizzes')

     def __str__(self):
        return f"{self.title} - {self.section.section_name}"

class Student(models.Model):
     name = models.CharField(max_length=100)
     student_id = models.CharField(max_length=20, unique=True)
     section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='students')

     def __str__(self):
         return f"{self.student_id}"

class Marks(models.Model):
     student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='marks')
     quiz = models.ForeignKey(Quizs, on_delete=models.CASCADE, related_name='marks')
     marks = models.DecimalField(max_digits=5, decimal_places=2)

     class Meta:
         unique_together = ('student', 'quiz')  # Ensure unique marks per quiz for each student

     def __str__(self):
         return f"{self.student.name} - {self.quiz.title}: {self.marks}"