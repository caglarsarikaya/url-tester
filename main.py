"""
URL Tester Application - Refactored Version
Entry point for the URL testing application.
"""

import sys
import logging
from src.application import URLTestApplication
from src.models import TestConfig


# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass


def main():
    """Main entry point"""
    try:
        print("=" * 60)
        print("           URL TESTER APPLICATION")
        print("=" * 60)
        print("\n⚠️  Press Ctrl+C at any time to stop testing")
        print("=" * 60)
        print("\nSelect testing mode:")
        print("  1. Defined URL list (from urls_to_test.xlsx)")
        print("  2. Sitemap parsing (from sitemaps.xlsx)")
        print()
        
        # Get user choice
        while True:
            choice = input("Enter your choice (1 or 2): ").strip()
            if choice in ['1', '2']:
                break
            print("Invalid choice. Please enter 1 or 2.")
        
        # Set mode based on choice
        mode = "defined" if choice == "1" else "sitemap"
        
        print()
        print("=" * 60)
        print("\n⚙️  Configuration (press Enter for defaults):")
        
        # Get concurrent workers
        workers_input = input(f"  Concurrent threads [default: 50]: ").strip()
        max_workers = int(workers_input) if workers_input.isdigit() else 50
        
        # Get timeout in milliseconds
        timeout_input = input(f"  Request timeout in ms [default: 10000]: ").strip()
        timeout_ms = int(timeout_input) if timeout_input.isdigit() else 10000
        timeout = timeout_ms / 1000  # Convert to seconds for requests library
        
        # Get delay in milliseconds
        delay_input = input(f"  Delay between requests in ms [default: 100]: ").strip()
        delay_ms = int(delay_input) if delay_input.isdigit() else 100
        delay = delay_ms / 1000  # Convert to seconds for time.sleep()
        
        print()
        print(f"[INFO] Using: {max_workers} threads, {timeout_ms}ms timeout, {delay_ms}ms delay")
        print("=" * 60)
        
        # Create configuration
        config = TestConfig(
            max_workers=max_workers,
            timeout=timeout,
            delay=delay
        )
        
        # Create and run application
        app = URLTestApplication(mode=mode, config=config)
        app.run()
        
    except KeyboardInterrupt:
        print("\n\n" + "=" * 60)
        print("⚠️  TESTING STOPPED BY USER (Ctrl+C)")
        print("=" * 60)
        print("\n[INFO] Testing was interrupted")
        print("[INFO] Partial results may have been saved")
        print("\nPress Enter to exit...")
        try:
            input()
        except:
            pass
        sys.exit(0)
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        logging.error(f"Application error: {str(e)}", exc_info=True)
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    # Wait for user before closing
    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()

