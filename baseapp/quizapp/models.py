from django.db import models

class Batch(models.Model):
    batch_name = models.CharField(max_length=50, blank=False, null=False)
    course_name = models.CharField(max_length=50, blank=False, null=False)
    course_code = models.CharField(max_length=50, blank=False, null=False) 
    
    class Meta:
        verbose_name = "Batch"
        verbose_name_plural = "Batch"

    def __str__(self):
        return f"{self.batch_name}"

class Section(models.Model):
    section_name = models.CharField(max_length=50, blank=False, null=False)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='sections')
    
    class Meta:
        verbose_name = "Section"
        verbose_name_plural = "Sections"

    def __str__(self):
        return f"{self.section_name} ({self.batch.batch_name})"
    
    
class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True, null=False)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='students')
    
    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Student"

    def __str__(self):
        return f"{self.student_id}"

class Quiz(models.Model):
    quiz_name = models.CharField(max_length=50, blank=False, null=False)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='quizzes')

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"

    def __str__(self):
        return f"{self.quiz_name} - {self.section.section_name}"


class QuizResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='quiz_results')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='results')
    marks = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Quiz Result"
        verbose_name_plural = "Quiz Results"
        unique_together = ('student', 'quiz')  # Ensures a student has only one result per quiz

    def __str__(self):
        return f"{self.student.student_id} - {self.quiz.quiz_name}: {self.marks}"
