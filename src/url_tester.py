"""URL testing service with concurrent execution"""

import time
import threading
from typing import List
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import requests

from .models import URLTestRequest, TestResult, TestConfig


class URLTesterService:
    """Service for testing URLs concurrently"""
    
    def __init__(self, config: TestConfig):
        self.config = config
    
    def test_urls(self, url_requests: List[URLTestRequest]) -> List[TestResult]:
        """
        Test all URLs concurrently and return results
        
        Args:
            url_requests: List of URL test requests
            
        Returns:
            List of test results (only failures, not 200 OK responses)
        """
        total = len(url_requests)
        results = []
        completed = 0
        success_count = 0
        error_count = 0
        
        print(f"\n[INFO] Starting URL tests...")
        print(f"[INFO] Max concurrent requests: {self.config.max_workers}")
        if self.config.delay > 0:
            print(f"[INFO] Submission delay: {self.config.delay}s between URLs")
        else:
            print(f"[INFO] No submission delay - maximum speed")
        print(f"[INFO] Press Ctrl+C to stop testing at any time")
        print("=" * 60)
        
        start_time = time.time()
        lock = threading.Lock()
        
        def update_progress():
            nonlocal completed
            with lock:
                completed += 1
                # Show updates at intervals
                if completed == 1 or completed % 10 == 0 or completed == total:
                    progress = (completed / total) * 100
                    elapsed = time.time() - start_time
                    rate = completed / elapsed if elapsed > 0 else 0
                    print(f"Progress: {completed}/{total} ({progress:.1f}%) - "
                          f"Success: {success_count} | Errors: {error_count} | "
                          f"Rate: {rate:.1f} req/s")
        
        # Submit all tasks to thread pool
        with ThreadPoolExecutor(max_workers=self.config.max_workers) as executor:
            futures = {}
            
            print(f"[INFO] Submitting {total} URLs to thread pool...")
            
            for url_request in url_requests:
                future = executor.submit(self._test_single_url, url_request)
                futures[future] = url_request
            
            print(f"[INFO] All URLs submitted! Processing results as they complete...")
            
            # Process results as they complete
            try:
                for future in as_completed(futures):
                    url_request = futures[future]
                    try:
                        result = future.result()
                        
                        if result.is_success:
                            with lock:
                                success_count += 1
                        else:
                            with lock:
                                error_count += 1
                            results.append(result)
                        
                        update_progress()
                        
                    except Exception as e:
                        with lock:
                            error_count += 1
                        print(f"[ERROR] Exception processing {url_request.url}: {str(e)}")
                        update_progress()
            except KeyboardInterrupt:
                print("\n\n[WARNING] Stopping tests... (waiting for active requests to finish)")
                executor.shutdown(wait=False, cancel_futures=True)
                raise
        
        # Print summary
        elapsed = time.time() - start_time
        print("=" * 60)
        print(f"\n[OK] Testing complete!")
        print(f"  Total URLs tested: {total}")
        print(f"  Successful (200): {success_count}")
        print(f"  Errors: {error_count}")
        print(f"  Total time: {elapsed:.1f} seconds")
        print(f"  Average rate: {total/elapsed:.1f} requests/second")
        
        return results
    
    def _test_single_url(self, url_request: URLTestRequest) -> TestResult:
        """Test a single URL and return result"""
        full_url = url_request.get_full_url()
        
        try:
            response = requests.get(
                full_url,
                timeout=self.config.timeout,
                allow_redirects=True,
                headers={'User-Agent': self.config.user_agent}
            )
            
            status_code = response.status_code
            error_msg = '' if status_code == 200 else f'HTTP {status_code}'
            
            return TestResult(
                source_url=url_request.url,
                tested_url=full_url,
                status_code=status_code,
                error_message=error_msg,
                tested_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            
        except requests.exceptions.Timeout:
            return TestResult(
                source_url=url_request.url,
                tested_url=full_url,
                status_code='TIMEOUT',
                error_message='Request timed out',
                tested_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        except requests.exceptions.ConnectionError:
            return TestResult(
                source_url=url_request.url,
                tested_url=full_url,
                status_code='CONNECTION_ERROR',
                error_message='Connection failed',
                tested_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        except requests.exceptions.TooManyRedirects:
            return TestResult(
                source_url=url_request.url,
                tested_url=full_url,
                status_code='TOO_MANY_REDIRECTS',
                error_message='Too many redirects',
                tested_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        except Exception as e:
            return TestResult(
                source_url=url_request.url,
                tested_url=full_url,
                status_code='ERROR',
                error_message=str(e),
                tested_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )

