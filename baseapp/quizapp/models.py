# from django.db import models

# class Batch(models.Model):
#     id = models.AutoField(primary_key=True)
#     batch_name = models.CharField(max_length=50, blank=False, null=False)
#     course_name = models.CharField(max_length=50, blank=False, null=False)
#     course_code = models.CharField(max_length=50, blank=False, null=False) 
    
#     class Meta:
#         verbose_name = "Batch"
#         verbose_name_plural = "Batch"

#     def __str__(self):
#         return f"{self.batch_name}"

# class Section(models.Model):
#     section_name = models.CharField(max_length=50, blank=False, null=False)
#     batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='sections')
    
#     class Meta:
#         verbose_name = "Section"
#         verbose_name_plural = "Sections"
#         constraints = [
#             models.UniqueConstraint(fields=["section_name", "batch"], name="unique_section_per_batch")
#         ]

#     def __str__(self):
#         return f"{self.section_name} ({self.batch.batch_name})"
    
    
# class Student(models.Model):
#     student_id = models.CharField(max_length=20, null=False)
#     section = models.ManyToManyField(Section, related_name='students')
    
#     class Meta:
#         verbose_name = "Student"
#         verbose_name_plural = "Student"

#     def __str__(self):
#         return f"{self.student_id}"

# class Quiz(models.Model):
#     quiz_name = models.CharField(max_length=50, blank=False, null=False)
#     section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='quizzes')
#     course_code = models.CharField(max_length=50, blank=False, null=False)
#     class Meta:
#         verbose_name = "Quiz"
#         verbose_name_plural = "Quizes"
#         constraints = [
#         models.UniqueConstraint(fields=["quiz_name", "section"], name="unique_quiz_per_section"),
#         ]

#     def __str__(self):
#         return f"{self.quiz_name} - {self.section.section_name}"


# class QuizResult(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='quiz_results')
#     quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='results')
#     marks = models.DecimalField(max_digits=5, decimal_places=2, default=None)

#     class Meta:
#         verbose_name = "Quiz Result"
#         verbose_name_plural = "Quiz Results"
#         constraints = [
#             models.UniqueConstraint(fields=["student", "quiz"], name="unique_quiz_result_per_student")
#         ]

#     def __str__(self):
#         return f"{self.student.student_id} - {self.quiz.quiz_name}: {self.marks}"


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
        return f"{self.studentName} ({self.studentId})"

class Quiz(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks = models.PositiveIntegerField(default=0)
    quizNo = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"Quiz: {self.quizNo}-{self.subject.subjectName} {self.student.studentId}"

