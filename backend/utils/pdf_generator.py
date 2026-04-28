"""
PDF Report Generation for Student Performance Analytics
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import os
import tempfile

class StudentReportGenerator:
    """
    Generate comprehensive PDF reports for student performance
    """
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Setup custom styles for the report"""
        # Title style
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        
        # Subtitle style
        self.subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=colors.darkgreen
        )
        
        # Section header style
        self.section_style = ParagraphStyle(
            'SectionHeader',
            parent=self.styles['Heading3'],
            fontSize=14,
            spaceAfter=12,
            spaceBefore=20,
            textColor=colors.darkred
        )
        
        # Normal text with better spacing
        self.normal_style = ParagraphStyle(
            'CustomNormal',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            alignment=TA_LEFT
        )
    
    def generate_student_report(self, student_record, prediction_data=None, output_dir='reports'):
        """
        Generate comprehensive student performance report
        
        Args:
            student_record: StudentRecord model instance
            prediction_data: Latest prediction data (optional)
            output_dir: Output directory for PDF files
            
        Returns:
            str: Path to generated PDF file
        """
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"student_report_{student_record.student_id}_{timestamp}.pdf"
        filepath = os.path.join(output_dir, filename)
        
        # Create PDF document
        doc = SimpleDocTemplate(
            filepath,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Build report content
        story = []
        
        # Header
        story.extend(self._build_header(student_record))
        
        # Student Information
        story.extend(self._build_student_info(student_record))
        
        # Academic Performance
        story.extend(self._build_academic_performance(student_record))
        
        # Prediction Results (if available)
        if prediction_data:
            story.extend(self._build_prediction_section(prediction_data))
        
        # Performance Analysis
        story.extend(self._build_performance_analysis(student_record))
        
        # Recommendations
        story.extend(self._build_recommendations(student_record, prediction_data))
        
        # Footer
        story.extend(self._build_footer())
        
        # Build PDF
        doc.build(story)
        
        return filepath
    
    def _build_header(self, student_record):
        """Build report header"""
        content = []
        
        # Title
        title = Paragraph("🎓 Student Performance Report", self.title_style)
        content.append(title)
        content.append(Spacer(1, 12))
        
        # Subtitle with student name
        subtitle = Paragraph(f"Academic Analysis for {student_record.student_name}", self.subtitle_style)
        content.append(subtitle)
        content.append(Spacer(1, 20))
        
        # Report generation info
        report_info = f"Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}"
        info_para = Paragraph(report_info, self.normal_style)
        content.append(info_para)
        content.append(Spacer(1, 20))
        
        return content
    
    def _build_student_info(self, student_record):
        """Build student information section"""
        content = []
        
        # Section header
        header = Paragraph("📋 Student Information", self.section_style)
        content.append(header)
        
        # Student info table
        data = [
            ['Student ID:', student_record.student_id],
            ['Name:', student_record.student_name],
            ['Age:', f"{student_record.age} years"],
            ['Gender:', student_record.gender],
            ['Class Participation:', student_record.class_participation],
            ['Extracurricular Activities:', student_record.extracurricular_activity]
        ]
        
        table = Table(data, colWidths=[2*inch, 3*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (1, 0), (1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        content.append(table)
        content.append(Spacer(1, 20))
        
        return content
    
    def _build_academic_performance(self, student_record):
        """Build academic performance section"""
        content = []
        
        # Section header
        header = Paragraph("📊 Academic Performance", self.section_style)
        content.append(header)
        
        # Performance metrics table
        data = [
            ['Metric', 'Score', 'Status'],
            ['Internal Marks', f"{student_record.internal_marks}/100", self._get_grade_status(student_record.internal_marks)],
            ['Assignment Score', f"{student_record.assignment_score}/100", self._get_grade_status(student_record.assignment_score)],
            ['Final Exam Marks', f"{student_record.final_exam_marks}/100", self._get_grade_status(student_record.final_exam_marks)],
            ['Previous Semester', f"{student_record.previous_sem_marks}/100", self._get_grade_status(student_record.previous_sem_marks)],
            ['Attendance', f"{student_record.attendance_percentage}%", self._get_attendance_status(student_record.attendance_percentage)],
            ['Study Hours/Week', f"{student_record.study_hours} hours", self._get_study_hours_status(student_record.study_hours)]
        ]
        
        table = Table(data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        content.append(table)
        content.append(Spacer(1, 20))
        
        # Overall performance summary
        overall_avg = (student_record.internal_marks + student_record.assignment_score + student_record.final_exam_marks) / 3
        summary_text = f"<b>Overall Average:</b> {overall_avg:.1f}/100 ({self._get_grade_letter(overall_avg)})"
        summary = Paragraph(summary_text, self.normal_style)
        content.append(summary)
        content.append(Spacer(1, 15))
        
        return content
    
    def _build_prediction_section(self, prediction_data):
        """Build AI prediction section"""
        content = []
        
        # Section header
        header = Paragraph("🤖 AI Performance Prediction", self.section_style)
        content.append(header)
        
        # Prediction summary
        prediction_text = f"""
        <b>Prediction:</b> {prediction_data['prediction']}<br/>
        <b>Confidence:</b> {prediction_data['probability']:.1%}<br/>
        <b>Risk Level:</b> {prediction_data['risk_level']}<br/>
        <b>Model Used:</b> {prediction_data['model_used']}<br/>
        """
        
        prediction_para = Paragraph(prediction_text, self.normal_style)
        content.append(prediction_para)
        content.append(Spacer(1, 15))
        
        # Feedback section
        if 'feedback' in prediction_data:
            feedback_header = Paragraph("💬 AI Feedback & Recommendations", self.section_style)
            content.append(feedback_header)
            
            # Clean and format feedback
            feedback_text = prediction_data['feedback'].replace('\n', '<br/>')
            feedback_para = Paragraph(feedback_text, self.normal_style)
            content.append(feedback_para)
            content.append(Spacer(1, 15))
        
        return content
    
    def _build_performance_analysis(self, student_record):
        """Build performance analysis section"""
        content = []
        
        # Section header
        header = Paragraph("📈 Performance Analysis", self.section_style)
        content.append(header)
        
        # Strengths and areas for improvement
        strengths = self._identify_strengths(student_record)
        improvements = self._identify_improvements(student_record)
        
        # Strengths
        if strengths:
            strengths_header = Paragraph("<b>🌟 Strengths:</b>", self.normal_style)
            content.append(strengths_header)
            
            for strength in strengths:
                strength_item = Paragraph(f"• {strength}", self.normal_style)
                content.append(strength_item)
            
            content.append(Spacer(1, 10))
        
        # Areas for improvement
        if improvements:
            improvements_header = Paragraph("<b>🎯 Areas for Improvement:</b>", self.normal_style)
            content.append(improvements_header)
            
            for improvement in improvements:
                improvement_item = Paragraph(f"• {improvement}", self.normal_style)
                content.append(improvement_item)
            
            content.append(Spacer(1, 15))
        
        return content
    
    def _build_recommendations(self, student_record, prediction_data=None):
        """Build recommendations section"""
        content = []
        
        # Section header
        header = Paragraph("💡 Recommendations", self.section_style)
        content.append(header)
        
        recommendations = self._generate_recommendations(student_record, prediction_data)
        
        for i, recommendation in enumerate(recommendations, 1):
            rec_text = f"{i}. {recommendation}"
            rec_para = Paragraph(rec_text, self.normal_style)
            content.append(rec_para)
        
        content.append(Spacer(1, 20))
        
        return content
    
    def _build_footer(self):
        """Build report footer"""
        content = []
        
        # Disclaimer
        disclaimer = """
        <i>This report is generated by the Student Performance Analytics System. 
        The AI predictions are based on historical data and should be used as guidance only. 
        Individual circumstances and efforts can significantly impact actual outcomes.</i>
        """
        
        disclaimer_para = Paragraph(disclaimer, self.normal_style)
        content.append(disclaimer_para)
        content.append(Spacer(1, 10))
        
        # Contact info
        contact = "For questions about this report, please contact your academic advisor."
        contact_para = Paragraph(contact, self.normal_style)
        content.append(contact_para)
        
        return content
    
    def _get_grade_status(self, score):
        """Get grade status based on score"""
        if score >= 90:
            return "Excellent"
        elif score >= 80:
            return "Good"
        elif score >= 70:
            return "Satisfactory"
        elif score >= 60:
            return "Needs Improvement"
        else:
            return "Poor"
    
    def _get_grade_letter(self, score):
        """Get letter grade based on score"""
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"
    
    def _get_attendance_status(self, attendance):
        """Get attendance status"""
        if attendance >= 90:
            return "Excellent"
        elif attendance >= 80:
            return "Good"
        elif attendance >= 70:
            return "Satisfactory"
        else:
            return "Poor"
    
    def _get_study_hours_status(self, hours):
        """Get study hours status"""
        if hours >= 30:
            return "Excellent"
        elif hours >= 20:
            return "Good"
        elif hours >= 15:
            return "Adequate"
        else:
            return "Insufficient"
    
    def _identify_strengths(self, student_record):
        """Identify student strengths"""
        strengths = []
        
        if student_record.attendance_percentage >= 85:
            strengths.append("Consistent attendance")
        
        if student_record.class_participation == "Yes":
            strengths.append("Active class participation")
        
        if student_record.extracurricular_activity == "Yes":
            strengths.append("Engaged in extracurricular activities")
        
        if student_record.study_hours >= 25:
            strengths.append("Dedicated study schedule")
        
        if student_record.assignment_score >= 80:
            strengths.append("Strong assignment performance")
        
        if student_record.final_exam_marks >= 80:
            strengths.append("Excellent exam performance")
        
        return strengths
    
    def _identify_improvements(self, student_record):
        """Identify areas for improvement"""
        improvements = []
        
        if student_record.attendance_percentage < 80:
            improvements.append("Improve class attendance")
        
        if student_record.class_participation == "No":
            improvements.append("Increase class participation")
        
        if student_record.study_hours < 20:
            improvements.append("Increase study time")
        
        if student_record.assignment_score < 70:
            improvements.append("Focus on assignment quality")
        
        if student_record.internal_marks < 70:
            improvements.append("Strengthen understanding of course material")
        
        return improvements
    
    def _generate_recommendations(self, student_record, prediction_data=None):
        """Generate personalized recommendations"""
        recommendations = []
        
        # Academic recommendations
        if student_record.internal_marks < 70:
            recommendations.append("Schedule regular study sessions and seek help from instructors for difficult topics")
        
        if student_record.assignment_score < 75:
            recommendations.append("Start assignments early and seek feedback before submission")
        
        # Behavioral recommendations
        if student_record.attendance_percentage < 85:
            recommendations.append("Maintain consistent attendance to stay current with course material")
        
        if student_record.class_participation == "No":
            recommendations.append("Actively participate in class discussions to enhance understanding")
        
        if student_record.study_hours < 25:
            recommendations.append("Increase weekly study hours and create a structured study schedule")
        
        # Engagement recommendations
        if student_record.extracurricular_activity == "No":
            recommendations.append("Consider joining extracurricular activities for holistic development")
        
        # Prediction-based recommendations
        if prediction_data and prediction_data.get('risk_level') == 'High':
            recommendations.append("Seek immediate academic support and consider tutoring services")
        
        # Default recommendations if none specific
        if not recommendations:
            recommendations.extend([
                "Continue maintaining your current performance level",
                "Set specific academic goals for continuous improvement",
                "Regularly review and adjust your study strategies"
            ])
        
        return recommendations

# Utility functions for easy access
def generate_student_report(student_record, prediction_data=None):
    """
    Generate PDF report for a student
    
    Args:
        student_record: StudentRecord model instance
        prediction_data: Latest prediction data (optional)
        
    Returns:
        str: Path to generated PDF file
    """
    generator = StudentReportGenerator()
    return generator.generate_student_report(student_record, prediction_data)

if __name__ == "__main__":
    print("📄 PDF Report Generator")
    print("This module generates comprehensive PDF reports for student performance.")
    print("Use generate_student_report(student_record, prediction_data) to create reports.")