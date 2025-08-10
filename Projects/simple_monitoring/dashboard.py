"""
Simple Dashboard - Real-time Metrics + Scaling Recommendations
Clean, educational interface showing system status
"""
import time
import os
import argparse
from datetime import datetime
from simple_monitoring.metrics_collector import SimpleMetricsCollector

# Importa recomendaciones si están disponibles
try:
    from simple_monitoring.recommendations import ScalingRecommendations
    HAS_RECOMMENDATIONS = True
except ImportError:
    HAS_RECOMMENDATIONS = False

class SimpleDashboard:
    """
    Clean dashboard showing:
    - Real system metrics
    - Scaling recommendations (educational)
    """
    def __init__(self, redis_host='localhost', redis_port=6379, api_url="http://localhost:8000"):
        self.metrics_collector = SimpleMetricsCollector(redis_host, redis_port, api_url)
        if HAS_RECOMMENDATIONS:
            self.recommendations = ScalingRecommendations()
        self.refresh_interval = 3  # seconds
        
    def run(self, show_recommendations=True):
        print("🚀 SIMPLE MONITORING DASHBOARD")
        print("=" * 60)
        if show_recommendations and HAS_RECOMMENDATIONS:
            print("📊 Showing: Metrics + Scaling Recommendations (Educational)")
        else:
            print("📊 Showing: System Metrics Only")
        print("💡 Press Ctrl+C to exit")
        print("=" * 60)
        try:
            self._clear_screen()
            while True:
                print("\033[H", end='')  # Move cursor to top (avoid flicker)
                metrics = self.metrics_collector.collect_metrics()
                self._display_header()
                self._display_system_metrics(metrics)
                self._display_worker_metrics(metrics)
                if show_recommendations and HAS_RECOMMENDATIONS:
                    self._display_scaling_recommendations(metrics)
                self._display_footer()
                time.sleep(self.refresh_interval)
        except KeyboardInterrupt:
            print("\n\n👋 Dashboard stopped")
    
    def _clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def _display_header(self):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"📊 SYSTEM MONITORING DASHBOARD - {timestamp}")
        print("=" * 60)
    
    def _display_system_metrics(self, metrics):
        print("\n🖥️  SYSTEM METRICS")
        print("-" * 30)
        cpu = metrics.get('cpu_usage', 0)
        memory = metrics.get('memory_usage', 0)
        memory_gb = metrics.get('memory_available_gb', 0)
        cpu_icon = self._get_load_icon(cpu, 50, 80)
        memory_icon = self._get_load_icon(memory, 60, 85)
        print(f"🔥 CPU Usage:      {cpu_icon} {cpu:>6.1f}%")
        print(f"🧠 Memory Usage:   {memory_icon} {memory:>6.1f}% ({memory_gb:.1f}GB free)")
    
    def _display_worker_metrics(self, metrics):
        print("\n⚙️  WORKER METRICS")
        print("-" * 30)
        active = metrics.get('active_workers', 0)
        busy = metrics.get('busy_workers', 0)
        utilization = metrics.get('worker_utilization', 0)
        queue = metrics.get('queue_length', 0)
        success_rate = metrics.get('success_rate', 0)
        util_icon = self._get_load_icon(utilization * 100, 50, 80)
        queue_icon = "🟢" if queue == 0 else "🟡" if queue < 5 else "🔴"
        success_icon = "🟢" if success_rate >= 90 else "🟡" if success_rate >= 70 else "🔴"
        print(f"👥 Active Workers: {active:>3d}")
        print(f"⚡ Busy Workers:   {busy:>3d}")
        print(f"📈 Utilization:    {util_icon} {utilization:>6.1%}")
        print(f"📋 Queue Length:   {queue_icon} {queue:>3d} tasks")
        print(f"✅ Success Rate:   {success_icon} {success_rate:>6.1f}%")
    
    def _display_scaling_recommendations(self, metrics):
        print("\n🎓 SCALING RECOMMENDATIONS (Educational)")
        print("-" * 50)
        if HAS_RECOMMENDATIONS:
            recommendation = self.recommendations.analyze_metrics(metrics)
            # Icons
            action_icons = {'scale_up': '🔺', 'scale_down': '🔻', 'maintain': '🟢'}
            action_icon = action_icons.get(recommendation.action, '❓')
            urgency_icons = {'high': '🚨', 'medium': '⚠️', 'low': '💡', 'none': '✅'}
            urgency_icon = urgency_icons.get(recommendation.urgency, '❓')
            print(f"📊 Current Workers:    {recommendation.current_workers}")
            print(f"🎯 Recommended:        {recommendation.recommended_workers}")
            print(f"🎬 Action:             {action_icon} {recommendation.action.upper()}")
            print(f"📝 Reason:             {recommendation.reason}")
            print(f"🎯 Confidence:         {recommendatio
