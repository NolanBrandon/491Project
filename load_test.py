#!/usr/bin/env python3
"""
Load Testing Script for EasyFitness API
Simulates 20 concurrent users accessing various endpoints
"""

import requests
import time
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Tuple
from datetime import datetime
import json

# Configuration
BASE_URL = "http://localhost:8000/api"
CONCURRENT_USERS = 20
REQUESTS_PER_USER = 5

class LoadTester:
    def __init__(self):
        self.results = []
        self.session = requests.Session()

    def test_endpoint(self, method: str, endpoint: str, data: dict = None, description: str = "") -> Dict:
        """Test a single endpoint and record metrics"""
        url = f"{BASE_URL}{endpoint}"

        start_time = time.time()
        try:
            if method == "GET":
                response = self.session.get(url, timeout=10)
            elif method == "POST":
                response = self.session.post(url, json=data, timeout=10)
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

        # Test different endpoints
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
            result = self.test_endpoint(method, endpoint, data, description)
            result['user_id'] = user_id
            user_results.append(result)

        return user_results

    def run_load_test(self):
        """Run load test with concurrent users"""
        print(f"🚀 Starting Load Test")
        print(f"📊 Configuration:")
        print(f"   - Base URL: {BASE_URL}")
        print(f"   - Concurrent Users: {CONCURRENT_USERS}")
        print(f"   - Total Requests: {CONCURRENT_USERS * 9} (9 endpoints per user)")
        print(f"\n{'='*80}\n")

        start_time = time.time()

        # Run concurrent users
        with ThreadPoolExecutor(max_workers=CONCURRENT_USERS) as executor:
            futures = [executor.submit(self.simulate_user, i) for i in range(CONCURRENT_USERS)]

            for future in as_completed(futures):
                try:
                    user_results = future.result()
                    self.results.extend(user_results)
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
        print(f"\n{'='*80}")
        print(f"💾 Saving detailed results to load_test_results.json")

        with open('/Users/ivanflores/capstone/load_test_results.json', 'w') as f:
            json.dump({
                'summary': {
                    'total_duration': total_duration,
                    'total_requests': total_requests,
                    'successful_requests': successful_requests,
                    'failed_requests': failed_requests,
                    'requests_per_second': total_requests/total_duration,
                    'concurrent_users': CONCURRENT_USERS,
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
    tester = LoadTester()
    total_duration = tester.run_load_test()
    tester.generate_report(total_duration)

if __name__ == "__main__":
    main()
