"""
API Documentation Generator for Student Performance Analytics
"""

import json
from datetime import datetime

class APIDocumentationGenerator:
    """
    Generate comprehensive API documentation
    """
    
    def __init__(self):
        self.api_docs = {
            "info": {
                "title": "Student Performance Analytics API",
                "version": "1.0.0",
                "description": "Complete API for student performance prediction and analytics",
                "contact": {
                    "name": "API Support",
                    "email": "support@studentanalytics.com"
                }
            },
            "servers": [
                {
                    "url": "http://localhost:5000",
                    "description": "Development server"
                }
            ],
            "paths": {},
            "components": {
                "securitySchemes": {
                    "bearerAuth": {
                        "type": "http",
                        "scheme": "bearer",
                        "bearerFormat": "JWT"
                    }
                }
            }
        }
        
        self.setup_api_endpoints()
    
    def setup_api_endpoints(self):
        """Setup all API endpoint documentation"""
        
        # Authentication endpoints
        self.api_docs["paths"]["/api/auth/register"] = {
            "post": {
                "tags": ["Authentication"],
                "summary": "Register new user",
                "description": "Create a new user account with role-based access",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "required": ["email", "password", "full_name", "role"],
                                "properties": {
                                    "email": {"type": "string", "format": "email", "example": "student@example.com"},
                                    "password": {"type": "string", "minLength": 6, "example": "password123"},
                                    "full_name": {"type": "string", "example": "John Doe"},
                                    "role": {"type": "string", "enum": ["student", "faculty", "admin"], "example": "student"}
                                }
                            }
                        }
                    }
                },
                "responses": {
                    "201": {
                        "description": "User registered successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "success": {"type": "boolean", "example": True},
                                        "message": {"type": "string", "example": "User registered successfully"},
                                        "data": {
                                            "type": "object",
                                            "properties": {
                                                "user": {"$ref": "#/components/schemas/User"},
                                                "access_token": {"type": "string"},
                                                "refresh_token": {"type": "string"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "400": {"description": "Invalid input data"},
                    "409": {"description": "User already exists"}
                }
            }
        }
        
        self.api_docs["paths"]["/api/auth/login"] = {
            "post": {
                "tags": ["Authentication"],
                "summary": "User login",
                "description": "Authenticate user and receive access tokens",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "required": ["email", "password"],
                                "properties": {
                                    "email": {"type": "string", "format": "email", "example": "student@demo.com"},
                                    "password": {"type": "string", "example": "student123"}
                                }
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Login successful",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "success": {"type": "boolean", "example": True},
                                        "message": {"type": "string", "example": "Login successful"},
                                        "data": {
                                            "type": "object",
                                            "properties": {
                                                "user": {"$ref": "#/components/schemas/User"},
                                                "access_token": {"type": "string"},
                                                "refresh_token": {"type": "string"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "401": {"description": "Invalid credentials"}
                }
            }
        }
        
        self.api_docs["paths"]["/api/auth/me"] = {
            "get": {
                "tags": ["Authentication"],
                "summary": "Get current user",
                "description": "Get current authenticated user information",
                "security": [{"bearerAuth": []}],
                "responses": {
                    "200": {
                        "description": "User information retrieved",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "success": {"type": "boolean", "example": True},
                                        "data": {
                                            "type": "object",
                                            "properties": {
                                                "user": {"$ref": "#/components/schemas/User"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "401": {"description": "Unauthorized"}
                }
            }
        }
        
        # Student endpoints
        self.api_docs["paths"]["/api/student/dashboard"] = {
            "get": {
                "tags": ["Student"],
                "summary": "Get student dashboard",
                "description": "Get comprehensive dashboard data including performance metrics and predictions",
                "security": [{"bearerAuth": []}],
                "responses": {
                    "200": {
                        "description": "Dashboard data retrieved",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "success": {"type": "boolean", "example": True},
                                        "data": {
                                            "type": "object",
                                            "properties": {
                                                "student_info": {"$ref": "#/components/schemas/StudentRecord"},
                                                "performance_metrics": {"$ref": "#/components/schemas/PerformanceMetrics"},
                                                "latest_prediction": {"$ref": "#/components/schemas/PredictionResult"},
                                                "prediction_history": {
                                                    "type": "array",
                                                    "items": {"$ref": "#/components/schemas/PredictionResult"}
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "403": {"description": "Student access required"},
                    "404": {"description": "Student record not found"}
                }
            }
        }
        
        self.api_docs["paths"]["/api/student/predict"] = {
            "post": {
                "tags": ["Student"],
                "summary": "Get AI prediction",
                "description": "Generate AI-powered performance prediction for the student",
                "security": [{"bearerAuth": []}],
                "responses": {
                    "200": {
                        "description": "Prediction generated successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "success": {"type": "boolean", "example": True},
                                        "data": {
                                            "type": "object",
                                            "properties": {
                                                "prediction": {"$ref": "#/components/schemas/PredictionResult"},
                                                "log_id": {"type": "integer"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "503": {"description": "ML model not available"}
                }
            }
        }
        
        # Faculty endpoints
        self.api_docs["paths"]["/api/faculty/students"] = {
            "get": {
                "tags": ["Faculty"],
                "summary": "Get all students",
                "description": "Get paginated list of all students with filtering options",
                "security": [{"bearerAuth": []}],
                "parameters": [
                    {
                        "name": "page",
                        "in": "query",
                        "description": "Page number",
                        "schema": {"type": "integer", "default": 1}
                    },
                    {
                        "name": "per_page",
                        "in": "query",
                        "description": "Items per page",
                        "schema": {"type": "integer", "default": 20}
                    },
                    {
                        "name": "search",
                        "in": "query",
                        "description": "Search by name or student ID",
                        "schema": {"type": "string"}
                    },
                    {
                        "name": "result",
                        "in": "query",
                        "description": "Filter by result",
                        "schema": {"type": "string", "enum": ["Pass", "Fail"]}
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Students list retrieved",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "success": {"type": "boolean", "example": True},
                                        "data": {
                                            "type": "object",
                                            "properties": {
                                                "students": {
                                                    "type": "array",
                                                    "items": {"$ref": "#/components/schemas/StudentRecord"}
                                                },
                                                "pagination": {"$ref": "#/components/schemas/Pagination"},
                                                "statistics": {"$ref": "#/components/schemas/StudentStatistics"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "403": {"description": "Faculty access required"}
                }
            }
        }
        
        # Admin endpoints
        self.api_docs["paths"]["/api/admin/users"] = {
            "get": {
                "tags": ["Admin"],
                "summary": "Get all users",
                "description": "Get paginated list of all users with filtering options",
                "security": [{"bearerAuth": []}],
                "parameters": [
                    {
                        "name": "page",
                        "in": "query",
                        "description": "Page number",
                        "schema": {"type": "integer", "default": 1}
                    },
                    {
                        "name": "role",
                        "in": "query",
                        "description": "Filter by role",
                        "schema": {"type": "string", "enum": ["student", "faculty", "admin"]}
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Users list retrieved"
                    },
                    "403": {"description": "Admin access required"}
                }
            }
        }
        
        self.api_docs["paths"]["/api/admin/train-model"] = {
            "post": {
                "tags": ["Admin"],
                "summary": "Train ML model",
                "description": "Trigger machine learning model training",
                "security": [{"bearerAuth": []}],
                "responses": {
                    "200": {
                        "description": "Model training completed",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "success": {"type": "boolean", "example": True},
                                        "message": {"type": "string", "example": "Model training completed successfully"},
                                        "data": {
                                            "type": "object",
                                            "properties": {
                                                "best_model": {"type": "string", "example": "random_forest"},
                                                "best_f1_score": {"type": "number", "example": 0.95},
                                                "models_trained": {
                                                    "type": "array",
                                                    "items": {"type": "string"}
                                                },
                                                "training_date": {"type": "string", "format": "date-time"},
                                                "dataset_size": {"type": "integer"},
                                                "feature_count": {"type": "integer"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "400": {"description": "Insufficient data for training"},
                    "403": {"description": "Admin access required"}
                }
            }
        }
        
        # Setup schemas
        self.setup_schemas()
    
    def setup_schemas(self):
        """Setup data schemas"""
        self.api_docs["components"]["schemas"] = {
            "User": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "example": 1},
                    "email": {"type": "string", "format": "email", "example": "student@demo.com"},
                    "role": {"type": "string", "enum": ["student", "faculty", "admin"], "example": "student"},
                    "full_name": {"type": "string", "example": "John Doe"},
                    "is_active": {"type": "boolean", "example": True},
                    "created_at": {"type": "string", "format": "date-time"},
                    "updated_at": {"type": "string", "format": "date-time"}
                }
            },
            
            "StudentRecord": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "example": 1},
                    "student_id": {"type": "string", "example": "STU001"},
                    "student_name": {"type": "string", "example": "Alice Johnson"},
                    "gender": {"type": "string", "enum": ["Male", "Female"], "example": "Female"},
                    "age": {"type": "integer", "example": 20},
                    "study_hours": {"type": "integer", "example": 30},
                    "attendance_percentage": {"type": "integer", "example": 85},
                    "internal_marks": {"type": "integer", "example": 80},
                    "assignment_score": {"type": "integer", "example": 85},
                    "previous_sem_marks": {"type": "integer", "example": 78},
                    "class_participation": {"type": "string", "enum": ["Yes", "No"], "example": "Yes"},
                    "extracurricular_activity": {"type": "string", "enum": ["Yes", "No"], "example": "Yes"},
                    "final_exam_marks": {"type": "integer", "example": 82},
                    "result": {"type": "string", "enum": ["Pass", "Fail"], "example": "Pass"}
                }
            },
            
            "PredictionResult": {
                "type": "object",
                "properties": {
                    "prediction": {"type": "string", "enum": ["Pass", "Fail"], "example": "Pass"},
                    "probability": {"type": "number", "example": 0.85},
                    "class_probabilities": {
                        "type": "object",
                        "properties": {
                            "Pass": {"type": "number", "example": 0.85},
                            "Fail": {"type": "number", "example": 0.15}
                        }
                    },
                    "risk_level": {"type": "string", "enum": ["Low", "Medium", "High"], "example": "Low"},
                    "feedback": {"type": "string", "example": "Great performance! Keep up the good work."},
                    "model_used": {"type": "string", "example": "random_forest"},
                    "prediction_date": {"type": "string", "format": "date-time"}
                }
            },
            
            "PerformanceMetrics": {
                "type": "object",
                "properties": {
                    "overall_score": {"type": "number", "example": 82.5},
                    "attendance_rate": {"type": "integer", "example": 85},
                    "study_hours_per_week": {"type": "integer", "example": 30},
                    "participation_level": {"type": "string", "example": "Yes"},
                    "extracurricular_involvement": {"type": "string", "example": "Yes"}
                }
            },
            
            "Pagination": {
                "type": "object",
                "properties": {
                    "page": {"type": "integer", "example": 1},
                    "per_page": {"type": "integer", "example": 20},
                    "total": {"type": "integer", "example": 100},
                    "pages": {"type": "integer", "example": 5},
                    "has_next": {"type": "boolean", "example": True},
                    "has_prev": {"type": "boolean", "example": False}
                }
            },
            
            "StudentStatistics": {
                "type": "object",
                "properties": {
                    "total_students": {"type": "integer", "example": 100},
                    "pass_count": {"type": "integer", "example": 85},
                    "fail_count": {"type": "integer", "example": 15},
                    "pass_rate": {"type": "number", "example": 85.0}
                }
            }
        }
    
    def generate_markdown_docs(self):
        """Generate markdown documentation"""
        markdown = f"""# Student Performance Analytics API Documentation

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Overview

{self.api_docs['info']['description']}

**Version:** {self.api_docs['info']['version']}

## Base URL

```
{self.api_docs['servers'][0]['url']}
```

## Authentication

This API uses JWT Bearer token authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

## Demo Accounts

| Role    | Email            | Password   |
|---------|------------------|------------|
| Student | student@demo.com | student123 |
| Faculty | faculty@demo.com | faculty123 |
| Admin   | admin@demo.com   | admin123   |

## Endpoints

### Authentication

#### POST /api/auth/register
Register a new user account.

**Request Body:**
```json
{{
  "email": "user@example.com",
  "password": "password123",
  "full_name": "John Doe",
  "role": "student"
}}
```

**Response:**
```json
{{
  "success": true,
  "message": "User registered successfully",
  "data": {{
    "user": {{ ... }},
    "access_token": "jwt-token",
    "refresh_token": "refresh-token"
  }}
}}
```

#### POST /api/auth/login
Authenticate user and receive tokens.

**Request Body:**
```json
{{
  "email": "student@demo.com",
  "password": "student123"
}}
```

#### GET /api/auth/me
Get current user information (requires authentication).

### Student Endpoints

#### GET /api/student/dashboard
Get comprehensive dashboard data including performance metrics and AI predictions.

**Headers:** `Authorization: Bearer <token>`

**Response:**
```json
{{
  "success": true,
  "data": {{
    "student_info": {{ ... }},
    "performance_metrics": {{ ... }},
    "latest_prediction": {{ ... }},
    "prediction_history": [...]
  }}
}}
```

#### POST /api/student/predict
Generate AI-powered performance prediction.

**Headers:** `Authorization: Bearer <token>`

#### GET /api/student/performance
Get detailed performance analytics and trends.

#### GET /api/student/report/download
Generate and download PDF performance report.

### Faculty Endpoints

#### GET /api/faculty/students
Get paginated list of all students with filtering options.

**Query Parameters:**
- `page` (integer): Page number (default: 1)
- `per_page` (integer): Items per page (default: 20)
- `search` (string): Search by name or student ID
- `result` (string): Filter by Pass/Fail

#### PUT /api/faculty/student/:id/update
Update student marks and information.

#### POST /api/faculty/upload-dataset
Upload CSV/Excel dataset for batch student data import.

#### GET /api/faculty/analytics
Get comprehensive analytics data for faculty dashboard.

### Admin Endpoints

#### GET /api/admin/users
Get paginated list of all users with role filtering.

#### PUT /api/admin/user/:id
Update user information and roles.

#### DELETE /api/admin/user/:id
Deactivate user account (soft delete).

#### POST /api/admin/train-model
Trigger machine learning model training.

**Response:**
```json
{{
  "success": true,
  "message": "Model training completed successfully",
  "data": {{
    "best_model": "random_forest",
    "best_f1_score": 0.95,
    "models_trained": ["logistic_regression", "random_forest", "xgboost"],
    "training_date": "2026-04-28T23:00:00",
    "dataset_size": 1200,
    "feature_count": 18
  }}
}}
```

#### GET /api/admin/system-insights
Get comprehensive system insights and statistics.

## Error Responses

All endpoints return consistent error responses:

```json
{{
  "success": false,
  "message": "Error description",
  "error": "detailed_error_code"
}}
```

### Common HTTP Status Codes

- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `409` - Conflict
- `500` - Internal Server Error
- `503` - Service Unavailable

## Rate Limiting

Currently no rate limiting is implemented, but it's recommended for production use.

## Data Models

### User
```json
{{
  "id": 1,
  "email": "student@demo.com",
  "role": "student",
  "full_name": "John Doe",
  "is_active": true,
  "created_at": "2026-04-28T10:00:00",
  "updated_at": "2026-04-28T10:00:00"
}}
```

### Student Record
```json
{{
  "id": 1,
  "student_id": "STU001",
  "student_name": "Alice Johnson",
  "gender": "Female",
  "age": 20,
  "study_hours": 30,
  "attendance_percentage": 85,
  "internal_marks": 80,
  "assignment_score": 85,
  "previous_sem_marks": 78,
  "class_participation": "Yes",
  "extracurricular_activity": "Yes",
  "final_exam_marks": 82,
  "result": "Pass"
}}
```

### Prediction Result
```json
{{
  "prediction": "Pass",
  "probability": 0.85,
  "class_probabilities": {{
    "Pass": 0.85,
    "Fail": 0.15
  }},
  "risk_level": "Low",
  "feedback": "Great performance! Keep up the good work.",
  "model_used": "random_forest",
  "prediction_date": "2026-04-28T23:00:00"
}}
```

## Testing

Use the provided test suite to verify API functionality:

```bash
python tests/test_api_routes.py
```

## Support

For API support and questions, please contact the development team.

---

**Generated by Student Performance Analytics API Documentation Generator**
"""
        return markdown
    
    def save_documentation(self, format='both'):
        """Save documentation in specified format(s)"""
        if format in ['json', 'both']:
            with open('api_documentation.json', 'w') as f:
                json.dump(self.api_docs, f, indent=2)
            print("✅ JSON documentation saved to api_documentation.json")
        
        if format in ['markdown', 'both']:
            markdown_docs = self.generate_markdown_docs()
            with open('API_DOCUMENTATION.md', 'w') as f:
                f.write(markdown_docs)
            print("✅ Markdown documentation saved to API_DOCUMENTATION.md")

def generate_api_documentation():
    """Generate comprehensive API documentation"""
    generator = APIDocumentationGenerator()
    generator.save_documentation('both')
    return generator.api_docs

if __name__ == "__main__":
    print("📚 Generating API Documentation...")
    generate_api_documentation()
    print("🎉 API documentation generated successfully!")