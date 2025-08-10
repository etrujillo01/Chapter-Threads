#!/usr/bin/env python3
"""
Simple Monitoring CLI - Adaptado a tu API real
"""
import time
import argparse
import requests
from datetime import datetime
import psutil

DEFAULT_API_URL = 'http://localhost:8000'

class SimpleMonitoringCLI:
    def __init__(self, api_url=DEFAULT_API_URL):
        self.api_url = api_url.rstrip('/')

    def check_api(self):
        """Check if API root is available"""
        try:
            response = requests.get(f'{self.api_url}/', timeout=5)
            if response.status_code == 200:
                print("✅ API is healthy and running")
                return True
            else:
                print(f"⚠️ API returned status {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ API not available: {e}")
            return False

    def show_metrics(self):
        """Display system metrics + workers via cluster/status endpoint"""
        try:
            # System metrics local
            cpu = psutil.cpu_percent(interval=1)
            mem = psutil.virtual_memory()
            # Worker info via API
            response = requests.get(f'{self.api_url}/cluster/status/', timeout=5)
            if response.status_code == 200:
                data = response.json()
                workers = data.get('active_workers', [])
                worker_count = data.get('count', 0)
            else:
                workers, worker_count = [], 0
            # Print everything
            self._display_metrics(cpu, mem, worker_count, workers)
            self._display_recommendation(worker_count)
        except Exception as e:
            print(f"❌ Error getting metrics: {e}")

    def monitor_live(self, duration=60):
        print(f"🔄 Live monitoring for {duration} seconds...")
        print("💡 Press Ctrl+C to stop early")
        print("=" * 50)
        start_time = time.time()
        try:
            while time.time() - start_time < duration:
                timestamp = datetime.now().strftime("%H:%M:%S")
                print(f"\n⏰ {timestamp}")
                print("-" * 20)
                self.show_metrics()
                print(f"\n🔄 Next update in 5 seconds...")
                time.sleep(5)
        except KeyboardInterrupt:
            print("\n\n👋 Live monitoring stopped")

    def run_stress(self, count=10, filters=None):
        """Stress: Launches N requests with images to /api/process/"""
        if filters is None:
            filters = ['resize', 'blur', 'brightness']
        print(f"🔥 Running stress test: {count} images with filters {filters}")
        img_path = 'static/images/sample_4k.jpg'  # Cambia si usas otro nombre/ruta
        results = []
        from threading import Thread
        def send_task(idx):
            try:
                with open(img_path, "rb") as f:
                    files = {"image": f}
                    data = {"filters": ','.join(filters)}
                    r = requests.post(f"{self.api_url}/api/process/", files=files, data=data, timeout=20)
                    results.append(r.status_code)
                    print(f"Tarea {idx} -> status {r.status_code}")
            except Exception as e:
                print(f"Tarea {idx} -> ERROR: {e}")
                results.append('ERR')
        threads = []
        t0 = time.time()
        for i in range(count):
            t = Thread(target=send_task, args=(i,))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
        t1 = time.time()
        print("\n📊 STRESS TEST RESULTS")
        print("=" * 40)
        print(f"⏱️  Total Time:   {t1 - t0:.2f}s")
        print(f"🖼️  Images:       {count}")
        print(f"✅ Success:      {results.count(200)}")
        print(f"❌ Errors:       {results.count('ERR') + sum(1 for s in results if s != 200)}")
        print(f"📈 Success Rate: {(results.count(200)/count)*100:.1f}%")

    def _display_metrics(self, cpu, mem, worker_count, workers):
        print("\n📊 SYSTEM METRICS")
        print("=" * 40)
        print(f"🔥 CPU Usage:         {cpu:>6.1f}%")
        print(f"🧠 Memory Usage:      {mem.percent:>6.1f}%")
        print(f"💽 Memory Available:  {mem.available/1024/1024/1024:>6.2f} GB")
        print("\n⚙️ WORKER METRICS")
        print("-" * 20)
        print(f"👥 Active Workers:    {worker_count:>6d}")
        print(f"🆔 Worker IDs:        {', '.join(workers) if workers else 'N/A'}")

    def _display_recommendation(self, worker_count):
        print(f"\n🎓 SCALING RECOMMENDATION (Educational)")
        print("-" * 40)
        if worker_count < 2:
            print("🚨 Recomendación: Aumentar workers. Hay riesgo de cuello de botella.")
        elif worker_count < 4:
            print("🟢 Recomendación: Mantener o escalar suavemente según la carga.")
        else:
            print("✅ Recomendación: Escalabilidad óptima para pruebas actuales.")
        print("💡 Nota: Las recomendaciones son educativas. Decide según tu monitoreo real.")

def main():
    parser = argparse.ArgumentParser(description='Simple Monitoring CLI')
    parser.add_argument('--api-url', default=DEFAULT_API_URL, help='API URL (default: http://localhost:8000)')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    subparsers.add_parser('check', help='Check API status')
    subparsers.add_parser('metrics', help='Show current metrics')

    monitor_parser = subparsers.add_parser('monitor', help='Live monitoring')
    monitor_parser.add_argument('--duration', type=int, default=60, help='Duration in seconds (default: 60)')

    stress_parser = subparsers.add_parser('stress', help='Generate stress load')
    stress_parser.add_argument('--count', type=int, default=10, help='Number of images (default: 10)')
    stress_parser.add_argument('--filters', nargs='+', default=['resize', 'blur', 'brightness'], help='Filters to apply')

    args = parser.parse_args()
    cli = SimpleMonitoringCLI(args.api_url)

    if args.command == 'check':
        cli.check_api()
    elif args.command == 'metrics':
        cli.show_metrics()
    elif args.command == 'monitor':
        cli.monitor_live(args.duration)
    elif args.command == 'stress':
        cli.run_stress(args.count, args.filters)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
