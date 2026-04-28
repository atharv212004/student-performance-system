"""
Sample data for testing the ML pipeline and API endpoints
"""

# Sample student records for testing
SAMPLE_STUDENTS = [
    {
        "student_id": "TEST001",
        "student_name": "Alice Johnson",
        "gender": "Female",
        "age": 20,
        "study_hours": 35,
        "attendance_percentage": 95,
        "internal_marks": 88,
        "assignment_score": 92,
        "previous_sem_marks": 85,
        "class_participation": "Yes",
        "extracurricular_activity": "Yes",
        "final_exam_marks": 89,
        "expected_result": "Pass"
    },
    {
        "student_id": "TEST002", 
        "student_name": "Bob Smith",
        "gender": "Male",
        "age": 21,
        "study_hours": 15,
        "attendance_percentage": 65,
        "internal_marks": 45,
        "assignment_score": 50,
        "previous_sem_marks": 48,
        "class_participation": "No",
        "extracurricular_activity": "No",
        "final_exam_marks": 42,
        "expected_result": "Fail"
    },
    {
        "student_id": "TEST003",
        "student_name": "Carol Davis",
        "gender": "Female", 
        "age": 19,
        "study_hours": 28,
        "attendance_percentage": 82,
        "internal_marks": 75,
        "assignment_score": 78,
        "previous_sem_marks": 72,
        "class_participation": "Yes",
        "extracurricular_activity": "No",
        "final_exam_marks": 76,
        "expected_result": "Pass"
    },
    {
        "student_id": "TEST004",
        "student_name": "David Wilson",
        "gender": "Male",
        "age": 22,
        "study_hours": 20,
        "attendance_percentage": 70,
        "internal_marks": 58,
        "assignment_score": 62,
        "previous_sem_marks": 55,
        "class_participation": "No",
        "extracurricular_activity": "Yes",
        "final_exam_marks": 59,
        "expected_result": "Pass"
    },
    {
        "student_id": "TEST005",
        "student_name": "Eva Martinez",
        "gender": "Female",
        "age": 20,
        "study_hours": 40,
        "attendance_percentage": 98,
        "internal_marks": 95,
        "assignment_score": 97,
        "previous_sem_marks": 93,
        "class_participation": "Yes",
        "extracurricular_activity": "Yes",
        "final_exam_marks": 96,
        "expected_result": "Pass"
    }
]

# Sample prediction requests for API testing
SAMPLE_PREDICTION_REQUESTS = [
    {
        "gender": "Female",
        "age": 20,
        "study_hours": 30,
        "attendance_percentage": 85,
        "internal_marks": 80,
        "assignment_score": 82,
        "previous_sem_marks": 78,
        "class_participation": "Yes",
        "extracurricular_activity": "Yes",
        "final_exam_marks": 81
    },
    {
        "gender": "Male",
        "age": 21,
        "study_hours": 12,
        "attendance_percentage": 60,
        "internal_marks": 40,
        "assignment_score": 45,
        "previous_sem_marks": 42,
        "class_participation": "No",
        "extracurricular_activity": "No",
        "final_exam_marks": 38
    }
]

def get_sample_students():
    """Get sample student data for testing"""
    return SAMPLE_STUDENTS

def get_sample_prediction_requests():
    """Get sample prediction requests for API testing"""
    return SAMPLE_PREDICTION_REQUESTS

def create_test_student_record(student_data):
    """Convert sample student data to StudentRecord format"""
    return {
        'user_id': 1,  # Default to first user
        'student_id': student_data['student_id'],
        'student_name': student_data['student_name'],
        'gender': student_data['gender'],
        'age': student_data['age'],
        'study_hours': student_data['study_hours'],
        'attendance_percentage': student_data['attendance_percentage'],
        'internal_marks': student_data['internal_marks'],
        'assignment_score': student_data['assignment_score'],
        'previous_sem_marks': student_data['previous_sem_marks'],
        'class_participation': student_data['class_participation'],
        'extracurricular_activity': student_data['extracurricular_activity'],
        'final_exam_marks': student_data['final_exam_marks'],
        'result': student_data.get('expected_result')
    }

if __name__ == "__main__":
    # Test sample data
    print("📊 Sample Student Data")
    print("="*50)
    
    students = get_sample_students()
    for i, student in enumerate(students, 1):
        print(f"\n{i}. {student['student_name']} ({student['student_id']})")
        print(f"   Age: {student['age']}, Gender: {student['gender']}")
        print(f"   Attendance: {student['attendance_percentage']}%")
        print(f"   Final Marks: {student['final_exam_marks']}")
        print(f"   Expected: {student['expected_result']}")
    
    print(f"\n✅ {len(students)} sample students available for testing")
    
    # Test prediction requests
    print(f"\n🔮 Sample Prediction Requests")
    print("="*50)
    
    requests = get_sample_prediction_requests()
    for i, req in enumerate(requests, 1):
        print(f"\n{i}. Student Profile:")
        print(f"   Age: {req['age']}, Gender: {req['gender']}")
        print(f"   Study Hours: {req['study_hours']}/week")
        print(f"   Attendance: {req['attendance_percentage']}%")
        print(f"   Final Marks: {req['final_exam_marks']}")
    
    print(f"\n✅ {len(requests)} sample prediction requests available")