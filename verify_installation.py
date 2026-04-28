#!/usr/bin/env python3
"""
Installation Verification Script
Checks if all components are properly installed and configured
"""

import os
import sys
import subprocess
from pathlib import Path

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(60)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.END}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ {text}{Colors.END}")

def check_python_version():
    """Check Python version"""
    print_info("Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print_success(f"Python {version.major}.{version.minor}.{version.micro} installed")
        return True
    else:
        print_error(f"Python 3.8+ required, found {version.major}.{version.minor}.{version.micro}")
        return False

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print_success(f"{description} found")
        return True
    else:
        print_error(f"{description} not found: {filepath}")
        return False

def check_directory_exists(dirpath, description):
    """Check if a directory exists"""
    if os.path.isdir(dirpath):
        print_success(f"{description} found")
        return True
    else:
        print_error(f"{description} not found: {dirpath}")
        return False

def check_backend_structure():
    """Check backend directory structure"""
    print_info("Checking backend structure...")
    
    checks = [
        ("backend/app.py", "Main Flask application"),
        ("backend/config.py", "Configuration file"),
        ("backend/requirements.txt", "Requirements file"),
        ("backend/models/db_models.py", "Database models"),
        ("backend/routes/auth_routes.py", "Auth routes"),
        ("backend/routes/student_routes.py", "Student routes"),
        ("backend/routes/faculty_routes.py", "Faculty routes"),
        ("backend/routes/admin_routes.py", "Admin routes"),
        ("backend/ml/train_model.py", "ML training script"),
        ("backend/ml/predict.py", "Prediction engine"),
        ("backend/ml/data_preprocessing.py", "Data preprocessing"),
        ("backend/utils/pdf_generator.py", "PDF generator"),
    ]
    
    results = [check_file_exists(path, desc) for path, desc in checks]
    
    dir_checks = [
        ("backend/ml/saved", "ML models directory"),
        ("backend/instance", "Database directory"),
    ]
    
    dir_results = [check_directory_exists(path, desc) for path, desc in dir_checks]
    
    return all(results + dir_results)

def check_frontend_structure():
    """Check frontend directory structure"""
    print_info("Checking frontend structure...")
    
    checks = [
        ("frontend/package.json", "Package.json"),
        ("frontend/vite.config.js", "Vite config"),
        ("frontend/tailwind.config.js", "Tailwind config"),
        ("frontend/src/App.jsx", "Main App component"),
        ("frontend/src/main.jsx", "Entry point"),
        ("frontend/src/services/api.js", "API service"),
        ("frontend/src/contexts/AuthContext.jsx", "Auth context"),
    ]
    
    results = [check_file_exists(path, desc) for path, desc in checks]
    
    dir_checks = [
        ("frontend/src/components", "Components directory"),
        ("frontend/src/pages", "Pages directory"),
        ("frontend/src/pages/student", "Student pages"),
        ("frontend/src/pages/faculty", "Faculty pages"),
        ("frontend/src/pages/admin", "Admin pages"),
        ("frontend/src/components/charts", "Chart components"),
    ]
    
    dir_results = [check_directory_exists(path, desc) for path, desc in dir_checks]
    
    return all(results + dir_results)

def check_python_packages():
    """Check if required Python packages are installed"""
    print_info("Checking Python packages...")
    
    required_packages = [
        'flask',
        'flask_sqlalchemy',
        'flask_jwt_extended',
        'flask_cors',
        'werkzeug',
        'pandas',
        'numpy',
        'scikit-learn',
        'xgboost',
        'reportlab',
        'openpyxl',
    ]
    
    all_installed = True
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print_success(f"{package} installed")
        except ImportError:
            print_error(f"{package} not installed")
            all_installed = False
    
    return all_installed

def check_node_modules():
    """Check if node_modules exists"""
    print_info("Checking Node.js dependencies...")
    
    if os.path.isdir("frontend/node_modules"):
        print_success("node_modules directory found")
        return True
    else:
        print_warning("node_modules not found. Run 'npm install' in frontend directory")
        return False

def check_database():
    """Check if database exists"""
    print_info("Checking database...")
    
    db_path = "backend/instance/student_performance.db"
    if os.path.exists(db_path):
        print_success("Database file found")
        
        # Check database size
        size = os.path.getsize(db_path)
        if size > 1000:  # More than 1KB means it has data
            print_success(f"Database has data ({size} bytes)")
            return True
        else:
            print_warning("Database exists but appears empty. Run 'python test_setup.py'")
            return False
    else:
        print_warning("Database not found. Run 'python test_setup.py' to create it")
        return False

def check_ml_models():
    """Check if ML models are trained"""
    print_info("Checking ML models...")
    
    model_files = [
        "backend/ml/saved/best_model.pkl",
        "backend/ml/saved/preprocessor.pkl",
        "backend/ml/saved/model_metadata.json",
    ]
    
    results = []
    for model_file in model_files:
        if os.path.exists(model_file):
            print_success(f"{os.path.basename(model_file)} found")
            results.append(True)
        else:
            print_warning(f"{os.path.basename(model_file)} not found")
            results.append(False)
    
    if not all(results):
        print_warning("Some models missing. Run 'python ml/train_model.py' in backend directory")
    
    return all(results)

def check_dataset():
    """Check if dataset exists"""
    print_info("Checking dataset...")
    
    if os.path.exists("clean_student_dataset.xlsx"):
        print_success("Dataset file found")
        return True
    else:
        print_error("Dataset file not found: clean_student_dataset.xlsx")
        return False

def check_documentation():
    """Check if documentation exists"""
    print_info("Checking documentation...")
    
    docs = [
        ("README.md", "Main README"),
        ("SETUP_INSTRUCTIONS.md", "Setup instructions"),
        ("PROJECT_COMPLETION_SUMMARY.md", "Completion summary"),
        ("QUICK_REFERENCE.md", "Quick reference"),
    ]
    
    results = [check_file_exists(path, desc) for path, desc in docs]
    return all(results)

def print_summary(results):
    """Print summary of checks"""
    print_header("VERIFICATION SUMMARY")
    
    total = len(results)
    passed = sum(results.values())
    failed = total - passed
    
    print(f"Total Checks: {total}")
    print_success(f"Passed: {passed}")
    if failed > 0:
        print_error(f"Failed: {failed}")
    
    print(f"\nSuccess Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print_success("\n✓ All checks passed! Your installation is complete.")
        print_info("\nNext steps:")
        print("  1. Start backend: cd backend && python app.py")
        print("  2. Start frontend: cd frontend && npm run dev")
        print("  3. Open browser: http://localhost:5173")
        print("  4. Login with demo accounts (see QUICK_REFERENCE.md)")
    else:
        print_warning("\n⚠ Some checks failed. Please review the errors above.")
        print_info("\nCommon fixes:")
        print("  - Install Python packages: pip install -r backend/requirements.txt")
        print("  - Install Node packages: cd frontend && npm install")
        print("  - Initialize database: cd backend && python test_setup.py")
        print("  - Train ML models: cd backend/ml && python train_model.py")
        print("\nFor detailed help, see SETUP_INSTRUCTIONS.md")

def main():
    """Main verification function"""
    print_header("INSTALLATION VERIFICATION")
    print_info("Verifying Student Performance Analytics System installation...\n")
    
    results = {}
    
    # Run all checks
    print_header("SYSTEM CHECKS")
    results['python_version'] = check_python_version()
    
    print_header("BACKEND CHECKS")
    results['backend_structure'] = check_backend_structure()
    results['python_packages'] = check_python_packages()
    results['database'] = check_database()
    results['ml_models'] = check_ml_models()
    
    print_header("FRONTEND CHECKS")
    results['frontend_structure'] = check_frontend_structure()
    results['node_modules'] = check_node_modules()
    
    print_header("DATA CHECKS")
    results['dataset'] = check_dataset()
    
    print_header("DOCUMENTATION CHECKS")
    results['documentation'] = check_documentation()
    
    # Print summary
    print_summary(results)
    
    return all(results.values())

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nVerification cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print_error(f"\nUnexpected error: {str(e)}")
        sys.exit(1)
