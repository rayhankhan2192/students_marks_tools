from django.db import models

class Batch(models.Model):
    batchName = models.CharField(max_length=50)

    def __str__(self):
        return self.batchName

class Section(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    sectionName = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.batch.batchName} - {self.sectionName}"

class Subject(models.Model):
    subjectName = models.CharField(max_length=100)
    subjectCode = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.subjectName} ({self.subjectCode})"

class Student(models.Model):
    studentId = models.CharField(max_length=50)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.studentId}"

class Quiz(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks = models.PositiveIntegerField(default=0)
    quizNo = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"Quiz: {self.quizNo}-{self.subject.subjectName} {self.student.studentId}"

