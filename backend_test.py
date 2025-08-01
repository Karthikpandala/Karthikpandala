#!/usr/bin/env python3
"""
Comprehensive Backend API Testing Suite for Portfolio Application
Tests all API endpoints with data validation and error handling
"""

import requests
import json
import sys
from datetime import datetime
from typing import Dict, List, Any

# Get backend URL from frontend .env file
def get_backend_url():
    try:
        with open('/app/frontend/.env', 'r') as f:
            for line in f:
                if line.startswith('REACT_APP_BACKEND_URL='):
                    return line.split('=', 1)[1].strip()
    except Exception as e:
        print(f"Error reading backend URL: {e}")
        return None

class PortfolioAPITester:
    def __init__(self):
        self.base_url = get_backend_url()
        if not self.base_url:
            raise Exception("Could not determine backend URL")
        
        self.api_url = f"{self.base_url}/api"
        self.test_results = []
        self.failed_tests = []
        
        print(f"Testing Portfolio API at: {self.api_url}")
        print("=" * 60)

    def log_test(self, test_name: str, success: bool, details: str = "", response_data: Any = None):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"    {details}")
        if not success and response_data:
            print(f"    Response: {response_data}")
        print()
        
        self.test_results.append({
            "test": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })
        
        if not success:
            self.failed_tests.append(test_name)

    def test_health_check(self):
        """Test API health check endpoint"""
        try:
            response = requests.get(f"{self.api_url}/", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("message") == "Portfolio API is running" and data.get("status") == "healthy":
                    self.log_test("API Health Check", True, "API is running and healthy")
                    return True
                else:
                    self.log_test("API Health Check", False, f"Unexpected response format: {data}")
                    return False
            else:
                self.log_test("API Health Check", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            self.log_test("API Health Check", False, f"Connection error: {str(e)}")
            return False

    def test_profile_api(self):
        """Test profile API endpoint"""
        try:
            response = requests.get(f"{self.api_url}/profile", timeout=10)
            
            if response.status_code == 200:
                profile = response.json()
                
                # Validate required fields
                required_fields = ["id", "name", "tagline", "bio", "contact"]
                missing_fields = [field for field in required_fields if field not in profile]
                
                if missing_fields:
                    self.log_test("Profile API - Structure", False, f"Missing fields: {missing_fields}")
                    return False
                
                # Validate contact information
                contact = profile.get("contact", {})
                contact_fields = ["email", "phone", "github", "linkedin"]
                missing_contact = [field for field in contact_fields if field not in contact]
                
                if missing_contact:
                    self.log_test("Profile API - Contact Info", False, f"Missing contact fields: {missing_contact}")
                    return False
                
                # Validate specific data matches resume
                expected_name = "Building Systems That See: Karthik Pandala"
                expected_email = "karthikpandala0502@gmail.com"
                expected_phone = "+91 8688262873"
                
                validation_errors = []
                if profile["name"] != expected_name:
                    validation_errors.append(f"Name mismatch: got '{profile['name']}', expected '{expected_name}'")
                
                if contact["email"] != expected_email:
                    validation_errors.append(f"Email mismatch: got '{contact['email']}', expected '{expected_email}'")
                
                if contact["phone"] != expected_phone:
                    validation_errors.append(f"Phone mismatch: got '{contact['phone']}', expected '{expected_phone}'")
                
                if validation_errors:
                    self.log_test("Profile API - Data Validation", False, "; ".join(validation_errors))
                    return False
                
                # Check for Computer Vision/AI focus in bio
                bio_lower = profile["bio"].lower()
                cv_keywords = ["computer vision", "ai", "opencv", "tensorflow", "pytorch"]
                found_keywords = [kw for kw in cv_keywords if kw in bio_lower]
                
                if not found_keywords:
                    self.log_test("Profile API - CV/AI Focus", False, "Bio doesn't mention Computer Vision/AI technologies")
                    return False
                
                self.log_test("Profile API", True, f"Profile data validated successfully. CV/AI keywords found: {found_keywords}")
                return True
                
            else:
                self.log_test("Profile API", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            self.log_test("Profile API", False, f"Connection error: {str(e)}")
            return False

    def test_skills_api(self):
        """Test skills API endpoint"""
        try:
            response = requests.get(f"{self.api_url}/skills", timeout=10)
            
            if response.status_code == 200:
                skills = response.json()
                
                # Validate structure
                if "categories" not in skills:
                    self.log_test("Skills API - Structure", False, "Missing 'categories' field")
                    return False
                
                categories = skills["categories"]
                if not isinstance(categories, list) or len(categories) == 0:
                    self.log_test("Skills API - Categories", False, "Categories should be a non-empty list")
                    return False
                
                # Validate category structure
                for i, category in enumerate(categories):
                    required_cat_fields = ["name", "items", "order"]
                    missing_cat_fields = [field for field in required_cat_fields if field not in category]
                    
                    if missing_cat_fields:
                        self.log_test("Skills API - Category Structure", False, 
                                    f"Category {i} missing fields: {missing_cat_fields}")
                        return False
                
                # Check for Computer Vision/AI category
                cv_category = None
                for category in categories:
                    if "computer vision" in category["name"].lower() or "ai" in category["name"].lower():
                        cv_category = category
                        break
                
                if not cv_category:
                    self.log_test("Skills API - CV/AI Category", False, "No Computer Vision/AI category found")
                    return False
                
                # Validate CV/AI skills
                cv_skills = cv_category["items"]
                expected_cv_skills = ["OpenCV", "TensorFlow", "PyTorch"]
                found_cv_skills = [skill for skill in expected_cv_skills if skill in cv_skills]
                
                if len(found_cv_skills) < 2:
                    self.log_test("Skills API - CV/AI Skills", False, 
                                f"Expected CV/AI skills not found. Found: {found_cv_skills}")
                    return False
                
                self.log_test("Skills API", True, 
                            f"Skills validated successfully. CV/AI skills found: {found_cv_skills}")
                return True
                
            else:
                self.log_test("Skills API", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            self.log_test("Skills API", False, f"Connection error: {str(e)}")
            return False

    def test_projects_api(self):
        """Test projects API endpoint"""
        try:
            response = requests.get(f"{self.api_url}/projects", timeout=10)
            
            if response.status_code == 200:
                projects = response.json()
                
                if not isinstance(projects, list):
                    self.log_test("Projects API - Structure", False, "Response should be a list")
                    return False
                
                if len(projects) == 0:
                    self.log_test("Projects API - Data", False, "No projects found")
                    return False
                
                # Validate project structure
                required_project_fields = ["id", "title", "description", "tech_stack", "features"]
                
                for i, project in enumerate(projects):
                    missing_fields = [field for field in required_project_fields if field not in project]
                    if missing_fields:
                        self.log_test("Projects API - Project Structure", False, 
                                    f"Project {i} missing fields: {missing_fields}")
                        return False
                
                # Check for Computer Vision projects
                cv_projects = []
                for project in projects:
                    title_desc = (project["title"] + " " + project["description"]).lower()
                    tech_stack_str = " ".join(project.get("tech_stack", [])).lower()
                    
                    cv_keywords = ["computer vision", "opencv", "gesture", "face recognition", "real-time"]
                    if any(keyword in title_desc or keyword in tech_stack_str for keyword in cv_keywords):
                        cv_projects.append(project["title"])
                
                if not cv_projects:
                    self.log_test("Projects API - CV Projects", False, "No Computer Vision projects found")
                    return False
                
                # Check for specific expected project
                time_quacker_found = any("time quacker" in project["title"].lower() for project in projects)
                if not time_quacker_found:
                    self.log_test("Projects API - Expected Project", False, "Time Quacker project not found")
                    return False
                
                self.log_test("Projects API", True, 
                            f"Projects validated successfully. CV projects found: {cv_projects}")
                return True
                
            else:
                self.log_test("Projects API", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            self.log_test("Projects API", False, f"Connection error: {str(e)}")
            return False

    def test_certificates_api(self):
        """Test certificates API endpoint"""
        try:
            response = requests.get(f"{self.api_url}/certificates", timeout=10)
            
            if response.status_code == 200:
                certificates = response.json()
                
                if not isinstance(certificates, list):
                    self.log_test("Certificates API - Structure", False, "Response should be a list")
                    return False
                
                if len(certificates) == 0:
                    self.log_test("Certificates API - Data", False, "No certificates found")
                    return False
                
                # Validate certificate structure
                required_cert_fields = ["id", "title", "issuer", "year", "description"]
                
                for i, cert in enumerate(certificates):
                    missing_fields = [field for field in required_cert_fields if field not in cert]
                    if missing_fields:
                        self.log_test("Certificates API - Certificate Structure", False, 
                                    f"Certificate {i} missing fields: {missing_fields}")
                        return False
                
                # Check for AI/Data Science certificates
                ai_certs = []
                for cert in certificates:
                    title_desc = (cert["title"] + " " + cert["description"]).lower()
                    ai_keywords = ["ai", "data science", "machine learning", "hackathon"]
                    
                    if any(keyword in title_desc for keyword in ai_keywords):
                        ai_certs.append(cert["title"])
                
                if not ai_certs:
                    self.log_test("Certificates API - AI/DS Certificates", False, "No AI/Data Science certificates found")
                    return False
                
                # Check for specific expected certificate
                hackathon_found = any("hackathon" in cert["title"].lower() for cert in certificates)
                if not hackathon_found:
                    self.log_test("Certificates API - Expected Certificate", False, "Hackathon certificate not found")
                    return False
                
                self.log_test("Certificates API", True, 
                            f"Certificates validated successfully. AI/DS certificates found: {ai_certs}")
                return True
                
            else:
                self.log_test("Certificates API", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            self.log_test("Certificates API", False, f"Connection error: {str(e)}")
            return False

    def test_education_api(self):
        """Test education API endpoint"""
        try:
            response = requests.get(f"{self.api_url}/education", timeout=10)
            
            if response.status_code == 200:
                education = response.json()
                
                if not isinstance(education, list):
                    self.log_test("Education API - Structure", False, "Response should be a list")
                    return False
                
                if len(education) == 0:
                    self.log_test("Education API - Data", False, "No education records found")
                    return False
                
                # Validate education structure
                required_edu_fields = ["id", "degree", "institution", "period", "grade"]
                
                for i, edu in enumerate(education):
                    missing_fields = [field for field in required_edu_fields if field not in edu]
                    if missing_fields:
                        self.log_test("Education API - Education Structure", False, 
                                    f"Education {i} missing fields: {missing_fields}")
                        return False
                
                # Check for Computer Science degree
                cs_degree_found = False
                for edu in education:
                    degree_lower = edu["degree"].lower()
                    if "computer science" in degree_lower or "cse" in degree_lower:
                        cs_degree_found = True
                        break
                
                if not cs_degree_found:
                    self.log_test("Education API - CS Degree", False, "Computer Science degree not found")
                    return False
                
                # Check for expected institution
                expected_institution = "Sri Indu College of Engineering and Technology"
                institution_found = any(expected_institution in edu["institution"] for edu in education)
                
                if not institution_found:
                    self.log_test("Education API - Expected Institution", False, 
                                f"Expected institution '{expected_institution}' not found")
                    return False
                
                self.log_test("Education API", True, "Education records validated successfully")
                return True
                
            else:
                self.log_test("Education API", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            self.log_test("Education API", False, f"Connection error: {str(e)}")
            return False

    def test_cors_headers(self):
        """Test CORS headers are properly set"""
        try:
            response = requests.options(f"{self.api_url}/", timeout=10)
            
            cors_headers = {
                'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
                'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
                'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers')
            }
            
            if cors_headers['Access-Control-Allow-Origin']:
                self.log_test("CORS Headers", True, "CORS headers are properly configured")
                return True
            else:
                self.log_test("CORS Headers", False, "CORS headers not found or improperly configured")
                return False
                
        except requests.exceptions.RequestException as e:
            self.log_test("CORS Headers", False, f"Connection error: {str(e)}")
            return False

    def run_all_tests(self):
        """Run all API tests"""
        print("Starting comprehensive Portfolio API testing...")
        print()
        
        # Test in order of dependency
        tests = [
            self.test_health_check,
            self.test_profile_api,
            self.test_skills_api,
            self.test_projects_api,
            self.test_certificates_api,
            self.test_education_api,
            self.test_cors_headers
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            if test():
                passed += 1
        
        print("=" * 60)
        print(f"TEST SUMMARY: {passed}/{total} tests passed")
        
        if self.failed_tests:
            print(f"FAILED TESTS: {', '.join(self.failed_tests)}")
        else:
            print("🎉 ALL TESTS PASSED!")
        
        print("=" * 60)
        
        return passed == total

def main():
    """Main test execution"""
    try:
        tester = PortfolioAPITester()
        success = tester.run_all_tests()
        
        # Save detailed results
        with open('/app/backend_test_results.json', 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'total_tests': len(tester.test_results),
                'passed_tests': len([t for t in tester.test_results if t['success']]),
                'failed_tests': len(tester.failed_tests),
                'results': tester.test_results
            }, f, indent=2)
        
        return 0 if success else 1
        
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())