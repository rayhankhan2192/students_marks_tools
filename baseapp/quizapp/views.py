from django.shortcuts import render
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from rest_framework import status, permissions, authentication
from rest_framework_simplejwt.authentication import JWTAuthentication


class BatchApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated] 
    def post(self, request):
        serializer = BatchSerializers(data=request.data, context={'request': request})  
        if serializer.is_valid():
            serializer.save()  # No need to pass auth_users manually, it's handled in serializer
            return Response({'message': 'Batch saved successfully!'}, status=status.HTTP_201_CREATED)
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        batches = Batch.objects.filter(auth_users = request.user)
        #batches = Batch.objects.all()
        serializer = BatchSerializers(batches, many = True)
        return Response(serializer.data, status =status.HTTP_200_OK)
    
class SectionApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        data = request.data
        serializer = SectionSerializers(data = data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Save Successfully!'}, status=status.HTTP_201_CREATED)
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    # def get(self, request):
    #     section = Section.objects.filter(auth_users = request.user)
    #     serializer = SectionSerializers(section, many = True)
    #     return Response(serializer.data, status =status.HTTP_200_OK)
    def get(self, request):
        sections = Section.objects.filter(auth_users = request.user)
        
        batch_id = request.query_params.get('batch_id')
        
        if batch_id:
            # sections = sections.filter(batch__batchName__icontains=batch_id) # query with exact batch name
            sections = sections.filter(batch_id=batch_id) # query with batch id
        serializer = SectionSerializers(sections, many = True)
        return Response(serializer.data, status =status.HTTP_200_OK)

class SubjectApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        data = request.data
        serializer = SubjectSerialisers(data = data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Save Successfully!'}, status=status.HTTP_201_CREATED)
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request):
        subjects = Subject.objects.filter(auth_users = request.user).select_related(
            'section__batch'
        )
        batch_id = request.query_params.get('batch')
        section_id = request.query_params.get('section')
        if batch_id:
            subjects = subjects.filter(batch_id = batch_id)
        if section_id:
            subjects = subjects.filter(section_id = section_id)
        if not subjects.exists():
            return Response({"message": "No data found!"})
        serializer = SubjectSerialisers(subjects, many = True)
        return Response(serializer.data, status =status.HTTP_200_OK)
    
class StudentApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        data = request.data
        serializer = StudentSerializers(data = data,  context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Save Successfully!'}, status=status.HTTP_201_CREATED)
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        subject_id = request.query_params.get('subject_id', None)
        section_id = request.query_params.get('section_id', None)
        batch_id = request.query_params.get('batch_id', None)
        
        students = Student.objects.filter(auth_users = request.user)
        
        if subject_id:
            students = students.filter(subject_id=subject_id)
        if section_id:
            students = students.filter(subject__section_id=section_id)
        if batch_id:
            students = students.filter(subject__batch_id=batch_id)
            
        serializer = StudentSerializers(students, many = True)
        return Response(serializer.data, status =status.HTTP_200_OK)
        
class QuizApiViews(APIView):
    def post(self, request):
        data = request.data
        serializer = QuizSerializers(data = data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Save Successfully!'}, status=status.HTTP_201_CREATED)
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        quizz = Quiz.objects.filter(auth_users = request.user).select_related(
            'student__section__batch', 'subject'
        )
        quizNo = request.query_params.get('quizNo')
        subject = request.query_params.get('subject')
        section = request.query_params.get('section')
        batch = request.query_params.get('batch')

        if quizNo:
            quizz = quizz.filter(quizNo=quizNo)
        if subject:
            quizz = quizz.filter(subject__subjectName__icontains=subject)
        if section:
            quizz = quizz.filter(student__section__sectionName__icontains=section)
        if batch:
            quizz = quizz.filter(student__section__batch__batchName__icontains=batch)
        if not quizz.exists():
            return Response(
                {"message": "No quiz data found for the given query."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = QuizGetSerializers(quizz, many = True)
        return Response(serializer.data, status =status.HTTP_200_OK)
    
        
    def put(self, request, *args, **kwargs):
        batch_name = request.query_params.get('batch_name')  
        section_name = request.query_params.get('section') 

        if not batch_name or not section_name:
            return Response({'message': 'Batch name and section are required for updating.'}, status=status.HTTP_400_BAD_REQUEST)

        student_id = request.data.get('student_id')  
        if not student_id:
            return Response({'message': 'Student ID is required for updating.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            student = Student.objects.get(
                section__batch_name=batch_name,
                section__section=section_name,
                student_id=student_id
            )
        except Student.DoesNotExist:
            return Response({'message': 'No student found with the given criteria.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = StudentSerializers(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Student updated successfully!', 'student': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, student_id, *args, **kwargs):
        try:
            student = Student.objects.get(student_id=student_id)
            student.delete()
            return Response({'message': 'Student deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
        except Student.DoesNotExist:
            return Response({'message': 'Student not found!'}, status=status.HTTP_404_NOT_FOUND)




"""garbage code"""
# class QuizApiView(APIView):
#     def post(self, request):
#         data = request.data
#         quiz_name = data.get("quiz_name")
#         section_name = data.get("section_name")
#         batch_name = data.get("batch_name")
        
#         if not quiz_name or not section_name or not batch_name:
#             return Response(
#                 {"message": "Fields 'quiz_name', 'section_name', and 'batch_name' are required."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#         try:
#             batch = Batch.objects.get(batch_name=batch_name)
#         except Batch.DoesNotExist:
#             return Response(
#                 {"message": f"Batch with name '{batch_name}' does not exist."},
#                 status=status.HTTP_404_NOT_FOUND,
#             )
#         try:
#             section = Section.objects.get(section_name=section_name, batch=batch)
#         except Section.DoesNotExist:
#             return Response(
#                 {
#                     "message": f"Section with name '{section_name}' does not exist in batch '{batch_name}'."
#                 },
#                 status=status.HTTP_404_NOT_FOUND,
#             )
#         quiz_data = {
#             'quiz_name': quiz_name,
#             'section': section.id
#         }
#         serializer = QuizCreateSerializers(data = quiz_data)
#         if serializer.is_valid():
#             serializer.save()
#         return Response(
#                 {"message": "Quiz create successfully."}, status=status.HTTP_201_CREATED
#             )
#         return Response({"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
#     def get(self, request):
#         batch_name = request.query_params.get('batch_name')  
#         section_name = request.query_params.get('section_name') 
#         course_code = request.query_params.get('course_code')
#         if not batch_name or not section_name or not course_code:
#             return Response(
#                 {"message": "Both 'batch_name' and 'section_name' are required."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#         try:
#             batch = Batch.objects.get(batch_name=batch_name, course_code = course_code)
#         except Batch.DoesNotExist:
#             return Response(
#                 {"message": f"Batch with name '{batch_name}' does not exist."},
#                 status=status.HTTP_404_NOT_FOUND,
#             )
#         try:
#             section = Section.objects.get(section_name=section_name, batch=batch)
#         except Section.DoesNotExist:
#             return Response(
#                 {
#                     "message": f"Section with name '{section_name}' does not exist in batch '{batch_name}'."
#                 },
#                 status=status.HTTP_404_NOT_FOUND,
#             )
#         students = Quiz.objects.filter(section=section)
#         if not students.exists():
#             return Response(
#                 {"message": "No students found in the specified batch and section."},
#                 status=status.HTTP_404_NOT_FOUND,
#             )
#         serializer = QuizSerializers(students, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)




# def get(self, request, *args, **kwargs):
    #     batch_name = request.query_params.get('batch')
    #     section_name = request.query_params.get('section')
    #     subject_code = request.query_params.get('subjectCode')
    #     quiz_no = request.query_params.get('quizNo')

    #     if not batch_name or not section_name or not quiz_no:
    #         return Response(
    #             {"message": "Parameters 'batch', 'section', and 'quizNo' are required."},
    #             status=status.HTTP_400_BAD_REQUEST,
    #         )

    #     try:
    #         batch = Batch.objects.get(batchName=batch_name)
    #     except Batch.DoesNotExist:
    #         return Response(
    #             {"message": f"Batch '{batch_name}' does not exist."},
    #             status=status.HTTP_404_NOT_FOUND,
    #         )

    #     try:
    #         section = Section.objects.get(sectionName=section_name, batch=batch)
    #     except Section.DoesNotExist:
    #         return Response(
    #             {"message": f"Section '{section_name}' does not exist in batch '{batch_name}'."},
    #             status=status.HTTP_404_NOT_FOUND,
    #         )

    #     students = Student.objects.filter(section=section)
    #     if not students.exists():
    #         return Response(
    #             {"message": "No students found in the specified batch and section."},
    #             status=status.HTTP_404_NOT_FOUND,
    #         )

    #     quiz_results = []
    #     for student in students:
    #         quizzes = Quiz.objects.filter(student=student, subject__subjectCode=subject_code, quizNo=quiz_no)

    #         for quiz in quizzes:
    #             quiz_results.append({
    #                 "quizNo": quiz.quizNo,
    #                 "studentId": student.studentId,
    #                 "batch": batch_name,
    #                 "section": section_name,
    #                 "subjectCode": subject_code,
    #                 "marks": quiz.marks
    #             })

    #     return Response(quiz_results, status=status.HTTP_200_OK)