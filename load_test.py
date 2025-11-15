#!/usr/bin/env python3
"""
Load Testing Script for EasyFitness API
Simulates 20 concurrent users accessing various endpoints
Includes authenticated and unauthenticated endpoint testing
Excludes AI-related endpoints
"""

import requests
import time
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Tuple
from datetime import datetime
import json
import uuid

# Configuration
BASE_URL = "http://localhost:8000/api"
CONCURRENT_USERS = 20
REQUESTS_PER_USER = 5

class LoadTester:
    def __init__(self, authenticated=False):
        self.results = []
        self.authenticated = authenticated
        self.test_users = []  # Store created test users

    def create_test_user(self, user_id: int) -> Dict:
        """Create a test user for load testing"""
        username = f"loadtest_user_{user_id}_{uuid.uuid4().hex[:8]}"
        email = f"{username}@loadtest.com"
        password = "TestPass123!"

        user_data = {
            "username": username,
            "email": email,
            "password": password,
            "password_confirm": password,
            "gender": "male" if user_id % 2 == 0 else "female",
            "date_of_birth": "1990-01-01"
        }

        try:
            response = requests.post(f"{BASE_URL}/users/", json=user_data, timeout=10)
            if response.status_code == 201:
                return {
                    'username': username,
                    'password': password,
                    'user_data': response.json()
                }
        except Exception as e:
            print(f"❌ Failed to create user {username}: {e}")

        return None

    def login_user(self, username: str, password: str) -> requests.Session:
        """Login user and return authenticated session"""
        session = requests.Session()

        login_data = {
            "username": username,
            "password": password
        }

        try:
            response = session.post(f"{BASE_URL}/users/login/", json=login_data, timeout=10)
            if response.status_code == 200:
                return session
        except Exception as e:
            print(f"❌ Failed to login user {username}: {e}")

        return None

    def test_endpoint(self, method: str, endpoint: str, session: requests.Session, data: dict = None, description: str = "") -> Dict:
        """Test a single endpoint and record metrics"""
        url = f"{BASE_URL}{endpoint}"

        start_time = time.time()
        try:
            if method == "GET":
                response = session.get(url, timeout=10)
            elif method == "POST":
                response = session.post(url, json=data, timeout=10)
            elif method == "PUT":
                response = session.put(url, json=data, timeout=10)
            elif method == "PATCH":
                response = session.patch(url, json=data, timeout=10)
            elif method == "DELETE":
                response = session.delete(url, timeout=10)
            else:
                raise ValueError(f"Unsupported method: {method}")

            end_time = time.time()
            response_time = (end_time - start_time) * 1000  # Convert to milliseconds

            return {
                'endpoint': endpoint,
                'method': method,
                'description': description,
                'status_code': response.status_code,
                'response_time_ms': response_time,
                'success': 200 <= response.status_code < 300,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            end_time = time.time()
            response_time = (end_time - start_time) * 1000
            return {
                'endpoint': endpoint,
                'method': method,
                'description': description,
                'status_code': 0,
                'response_time_ms': response_time,
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def simulate_user(self, user_id: int) -> List[Dict]:
        """Simulate a single user making multiple requests"""
        user_results = []
        session = requests.Session()

        # If authenticated mode, create user and login
        if self.authenticated:
            # Create and login user
            user_info = self.create_test_user(user_id)
            if not user_info:
                print(f"❌ Failed to create user for user_id {user_id}")
                return user_results

            session = self.login_user(user_info['username'], user_info['password'])
            if not session:
                print(f"❌ Failed to login user {user_info['username']}")
                return user_results

            user_db_id = user_info['user_data'].get('id')

            # Authenticated endpoints to test (excluding AI endpoints)
            endpoints_to_test = [
                ("GET", "/health/", None, "Health check"),
                ("GET", "/info/", None, "API info"),
                ("GET", "/users/", None, "List users"),
                ("GET", "/user-metrics/", None, "List user metrics"),
                ("GET", "/goals/", None, "List goals"),
                ("GET", "/nutrition-logs/", None, "List nutrition logs"),
                ("GET", "/workout-plans/", None, "List workout plans"),
                ("GET", "/workout-logs/", None, "List workout logs"),
                ("GET", "/meal-plans/", None, "List meal plans"),

                # Create operations
                ("POST", "/goals/", {
                    "title": f"Test Goal {user_id}",
                    "description": "Load test goal",
                    "goal_type": "weight_loss",
                    "target_weight_kg": 70.0,
                    "status": "active"
                }, "Create goal"),

                ("POST", "/user-metrics/", {
                    "weight_kg": 75.0,
                    "height_cm": 175.0,
                    "activity_level": "moderate"
                }, "Create user metrics"),

                ("POST", "/nutrition-logs/", {
                    "food_name": "Test Food",
                    "quantity": 100,
                    "meal_type": "lunch",
                    "calories": 200,
                    "protein": 10,
                    "carbs": 20,
                    "sugar": 5
                }, "Create nutrition log"),

                ("POST", "/workout-logs/", {
                    "exercise_name": "Test Exercise",
                    "duration_minutes": 30,
                    "calories_burned": 200,
                    "notes": "Load test workout"
                }, "Create workout log"),
            ]
        else:
            # Unauthenticated endpoints (same as before)
            endpoints_to_test = [
                ("GET", "/health/", None, "Health check"),
                ("GET", "/info/", None, "API info"),
                ("GET", "/users/", None, "List users"),
                ("GET", "/user-metrics/", None, "List user metrics"),
                ("GET", "/goals/", None, "List goals"),
                ("GET", "/nutrition-logs/", None, "List nutrition logs"),
                ("GET", "/workout-plans/", None, "List workout plans"),
                ("GET", "/workout-logs/", None, "List workout logs"),
                ("GET", "/meal-plans/", None, "List meal plans"),
            ]

        for method, endpoint, data, description in endpoints_to_test:
            result = self.test_endpoint(method, endpoint, session, data, description)
            result['user_id'] = user_id
            result['authenticated'] = self.authenticated
            user_results.append(result)

        return user_results

    def run_load_test(self):
        """Run load test with concurrent users"""
        mode = "AUTHENTICATED" if self.authenticated else "UNAUTHENTICATED"
        endpoints_count = 13 if self.authenticated else 9

        print(f"🚀 Starting {mode} Load Test")
        print(f"📊 Configuration:")
        print(f"   - Base URL: {BASE_URL}")
        print(f"   - Concurrent Users: {CONCURRENT_USERS}")
        print(f"   - Mode: {mode}")
        print(f"   - Total Requests: ~{CONCURRENT_USERS * endpoints_count} ({endpoints_count} endpoints per user)")
        print(f"\n{'='*80}\n")

        start_time = time.time()

        # Run concurrent users
        with ThreadPoolExecutor(max_workers=CONCURRENT_USERS) as executor:
            futures = [executor.submit(self.simulate_user, i) for i in range(CONCURRENT_USERS)]

            completed = 0
            for future in as_completed(futures):
                try:
                    user_results = future.result()
                    self.results.extend(user_results)
                    completed += 1
                    if self.authenticated:
                        print(f"✓ Completed user {completed}/{CONCURRENT_USERS}")
                except Exception as e:
                    print(f"❌ Error in user simulation: {e}")

        end_time = time.time()
        total_duration = end_time - start_time

        return total_duration

    def generate_report(self, total_duration: float):
        """Generate comprehensive performance report"""
        print(f"\n{'='*80}")
        print(f"📈 PERFORMANCE TEST REPORT")
        print(f"{'='*80}\n")

        # Overall statistics
        total_requests = len(self.results)
        successful_requests = sum(1 for r in self.results if r['success'])
        failed_requests = total_requests - successful_requests

        print(f"⏱️  Total Duration: {total_duration:.2f} seconds")
        print(f"📨 Total Requests: {total_requests}")
        print(f"✅ Successful: {successful_requests} ({successful_requests/total_requests*100:.1f}%)")
        print(f"❌ Failed: {failed_requests} ({failed_requests/total_requests*100:.1f}%)")
        print(f"🔄 Requests/Second: {total_requests/total_duration:.2f}")

        # Response time statistics
        response_times = [r['response_time_ms'] for r in self.results if r['success']]

        if response_times:
            print(f"\n{'='*80}")
            print(f"⚡ RESPONSE TIME STATISTICS")
            print(f"{'='*80}\n")
            print(f"Average: {statistics.mean(response_times):.2f} ms")
            print(f"Median: {statistics.median(response_times):.2f} ms")
            print(f"Min: {min(response_times):.2f} ms")
            print(f"Max: {max(response_times):.2f} ms")
            if len(response_times) > 1:
                print(f"Std Dev: {statistics.stdev(response_times):.2f} ms")

        # Per-endpoint statistics
        print(f"\n{'='*80}")
        print(f"🎯 PER-ENDPOINT PERFORMANCE")
        print(f"{'='*80}\n")

        endpoints = {}
        for result in self.results:
            key = f"{result['method']} {result['endpoint']}"
            if key not in endpoints:
                endpoints[key] = {
                    'description': result['description'],
                    'response_times': [],
                    'successes': 0,
                    'failures': 0,
                    'status_codes': {}
                }

            endpoints[key]['response_times'].append(result['response_time_ms'])
            if result['success']:
                endpoints[key]['successes'] += 1
            else:
                endpoints[key]['failures'] += 1

            status = result['status_code']
            endpoints[key]['status_codes'][status] = endpoints[key]['status_codes'].get(status, 0) + 1

        # Sort by average response time
        sorted_endpoints = sorted(
            endpoints.items(),
            key=lambda x: statistics.mean(x[1]['response_times'])
        )

        print(f"{'Endpoint':<40} {'Requests':<10} {'Avg (ms)':<12} {'Min (ms)':<12} {'Max (ms)':<12} {'Success Rate':<15}")
        print(f"{'-'*40} {'-'*10} {'-'*12} {'-'*12} {'-'*12} {'-'*15}")

        for endpoint, stats in sorted_endpoints:
            avg_time = statistics.mean(stats['response_times'])
            min_time = min(stats['response_times'])
            max_time = max(stats['response_times'])
            total = stats['successes'] + stats['failures']
            success_rate = (stats['successes'] / total * 100) if total > 0 else 0

            print(f"{endpoint:<40} {total:<10} {avg_time:<12.2f} {min_time:<12.2f} {max_time:<12.2f} {success_rate:<14.1f}%")

        # Status code distribution
        print(f"\n{'='*80}")
        print(f"📊 STATUS CODE DISTRIBUTION")
        print(f"{'='*80}\n")

        all_status_codes = {}
        for result in self.results:
            status = result['status_code']
            all_status_codes[status] = all_status_codes.get(status, 0) + 1

        for status, count in sorted(all_status_codes.items()):
            percentage = (count / total_requests * 100)
            print(f"Status {status}: {count} requests ({percentage:.1f}%)")

        # Save detailed results to JSON
        mode_suffix = "authenticated" if self.authenticated else "unauthenticated"
        filename = f'/Users/ivanflores/capstone/load_test_results_{mode_suffix}.json'

        print(f"\n{'='*80}")
        print(f"💾 Saving detailed results to {filename.split('/')[-1]}")

        with open(filename, 'w') as f:
            json.dump({
                'summary': {
                    'total_duration': total_duration,
                    'total_requests': total_requests,
                    'successful_requests': successful_requests,
                    'failed_requests': failed_requests,
                    'requests_per_second': total_requests/total_duration if total_duration > 0 else 0,
                    'concurrent_users': CONCURRENT_USERS,
                    'authenticated': self.authenticated,
                    'timestamp': datetime.now().isoformat()
                },
                'statistics': {
                    'average_response_time_ms': statistics.mean(response_times) if response_times else 0,
                    'median_response_time_ms': statistics.median(response_times) if response_times else 0,
                    'min_response_time_ms': min(response_times) if response_times else 0,
                    'max_response_time_ms': max(response_times) if response_times else 0,
                },
                'detailed_results': self.results
            }, f, indent=2)

        print(f"{'='*80}\n")

def main():
    import sys

    # Check command line arguments
    run_authenticated = True
    run_unauthenticated = True

    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        if mode == "auth":
            run_unauthenticated = False
        elif mode == "unauth":
            run_authenticated = False
        elif mode == "both":
            pass  # Run both
        else:
            print("Usage: python3 load_test.py [auth|unauth|both]")
            print("  auth   - Run only authenticated tests")
            print("  unauth - Run only unauthenticated tests")
            print("  both   - Run both tests (default)")
            sys.exit(1)

    # Run unauthenticated tests
    if run_unauthenticated:
        print("=" * 80)
        print("RUNNING UNAUTHENTICATED LOAD TESTS")
        print("=" * 80)
        tester_unauth = LoadTester(authenticated=False)
        duration_unauth = tester_unauth.run_load_test()
        tester_unauth.generate_report(duration_unauth)

    # Run authenticated tests
    if run_authenticated:
        print("\n\n")
        print("=" * 80)
        print("RUNNING AUTHENTICATED LOAD TESTS (Excluding AI endpoints)")
        print("=" * 80)
        tester_auth = LoadTester(authenticated=True)
        duration_auth = tester_auth.run_load_test()
        tester_auth.generate_report(duration_auth)

    print("\n" + "=" * 80)
    print("✅ LOAD TESTING COMPLETE")
    print("=" * 80)
    print("\nResults saved to:")
    if run_unauthenticated:
        print("  - load_test_results_unauthenticated.json")
    if run_authenticated:
        print("  - load_test_results_authenticated.json")
    print()

if __name__ == "__main__":
    main()
