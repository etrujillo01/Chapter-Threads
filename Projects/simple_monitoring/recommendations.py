"""
Scaling Recommendations System - Educational Only
Shows scaling algorithms and recommendations but NEVER executes anything
"""
from typing import Dict, Any, NamedTuple
from dataclasses import dataclass


@dataclass
class ScalingRecommendation:
    """A scaling recommendation (read-only)"""
    action: str  # 'scale_up', 'scale_down', 'maintain'
    current_workers: int
    recommended_workers: int
    reason: str
    confidence: float  # 0.0 - 1.0
    urgency: str  # 'low', 'medium', 'high'


class ScalingRecommendations:
    """
    Educational scaling recommendations system
    
    ⚠️  IMPORTANT: This system only provides RECOMMENDATIONS
    ⚠️  It NEVER executes any scaling actions
    ⚠️  Like AWS CloudWatch - suggests but doesn't execute
    """
    
    def __init__(self):
        # Scaling thresholds (educational values)
        self.min_workers = 1
        self.max_workers = 8
        
        # Scale UP thresholds
        self.scale_up_queue_threshold = 5      # tasks in queue
        self.scale_up_utilization_threshold = 0.8  # 80% worker utilization
        self.scale_up_cpu_threshold = 75.0     # 75% CPU
        
        # Scale DOWN thresholds  
        self.scale_down_queue_threshold = 0    # no queue
        self.scale_down_utilization_threshold = 0.3  # 30% utilization
        self.scale_down_cpu_threshold = 20.0   # 20% CPU
        
    def analyze_metrics(self, metrics: Dict[str, Any]) -> ScalingRecommendation:
        """
        Analyze metrics and provide scaling recommendation
        
        🎓 EDUCATIONAL: This shows how scaling algorithms work
        ⚠️  READ-ONLY: Does not execute any changes
        """
        current_workers = metrics.get('active_workers', 3)
        queue_length = metrics.get('queue_length', 0)
        utilization = metrics.get('worker_utilization', 0)
        cpu_usage = metrics.get('cpu_usage', 0)
        
        # ========================================
        # 🎓 EDUCATIONAL: Scale UP Logic
        # ========================================
        scale_up_reasons = []
        scale_up_confidence = 0.0
        
        # Check queue backlog
        if queue_length > self.scale_up_queue_threshold:
            scale_up_reasons.append(f"High queue: {queue_length} tasks")
            scale_up_confidence += 0.4
        
        # Check worker utilization (only if there's work waiting)
        if utilization > self.scale_up_utilization_threshold and queue_length > 0:
            scale_up_reasons.append(f"High utilization: {utilization:.1%}")
            scale_up_confidence += 0.3
        
        # Check CPU usage (only if there's work waiting)  
        if cpu_usage > self.scale_up_cpu_threshold and queue_length > 0:
            scale_up_reasons.append(f"High CPU: {cpu_usage:.1f}%")
            scale_up_confidence += 0.3
        
        # ========================================
        # 🎓 EDUCATIONAL: Scale DOWN Logic  
        # ========================================
        scale_down_reasons = []
        scale_down_confidence = 0.0
        
        # Check if system is underutilized
        if (queue_length <= self.scale_down_queue_threshold and 
            utilization < self.scale_down_utilization_threshold and
            cpu_usage < self.scale_down_cpu_threshold and
            current_workers > self.min_workers):
            
            scale_down_reasons.append(f"Low utilization: {utilization:.1%}")
            scale_down_reasons.append(f"No queue backlog")
            scale_down_confidence = 0.7
        
        # ========================================
        # 🎓 EDUCATIONAL: Make Recommendation
        # ========================================
        
        # Priority: Scale UP if needed
        if scale_up_reasons and current_workers < self.max_workers:
            recommended_workers = self._calculate_scale_up_target(
                current_workers, queue_length, utilization
            )
            return ScalingRecommendation(
                action='scale_up',
                current_workers=current_workers,
                recommended_workers=recommended_workers,
                reason=' + '.join(scale_up_reasons),
                confidence=min(scale_up_confidence, 1.0),
                urgency=self._get_urgency(scale_up_confidence)
            )
        
        # Scale DOWN if underutilized
        elif scale_down_reasons and current_workers > self.min_workers:
            recommended_workers = max(current_workers - 1, self.min_workers)
            return ScalingRecommendation(
                action='scale_down',
                current_workers=current_workers,
                recommended_workers=recommended_workers,
                reason=' + '.join(scale_down_reasons),
                confidence=scale_down_confidence,
                urgency='low'
            )
        
        # No scaling needed
        else:
            return ScalingRecommendation(
                action='maintain',
                current_workers=current_workers,
                recommended_workers=current_workers,
                reason='System operating within optimal parameters',
                confidence=0.8,
                urgency='none'
            )
    
    def _calculate_scale_up_target(self, current: int, queue: int, utilization: float) -> int:
        """
        🎓 EDUCATIONAL: Calculate target worker count for scale up
        
        This shows different scaling strategies:
        - Conservative: +1 worker at a time
        - Aggressive: Based on queue length  
        - Utilization-based: Based on current load
        """
        
        # Strategy 1: Conservative (default)
        if queue <= 3:
            target = current + 1
        
        # Strategy 2: Queue-based scaling
        elif queue <= 10:
            # Add 1 worker per 3 tasks in queue
            additional = (queue // 3) + 1
            target = current + additional
        
        # Strategy 3: Aggressive for high load
        else:
            # Add 1 worker per 2 tasks for very high load
            additional = (queue // 2) + 1
            target = current + additional
        
        # Cap at maximum
        return min(target, self.max_workers)
    
    def _get_urgency(self, confidence: float) -> str:
        """Convert confidence to urgency level"""
        if confidence >= 0.8:
            return 'high'
        elif confidence >= 0.5:
            return 'medium'
        else:
            return 'low'
    
    def get_scaling_config(self) -> Dict[str, Any]:
        """Get current scaling configuration (for transparency)"""
        return {
            'min_workers': self.min_workers,
            'max_workers': self.max_workers,
            'scale_up_thresholds': {
                'queue_length': self.scale_up_queue_threshold,
                'utilization': self.scale_up_utilization_threshold,
                'cpu_usage': self.scale_up_cpu_threshold
            },
            'scale_down_thresholds': {
                'queue_length': self.scale_down_queue_threshold,
                'utilization': self.scale_down_utilization_threshold,
                'cpu_usage': self.scale_down_cpu_threshold
            },
            'note': '⚠️ RECOMMENDATIONS ONLY - No automatic execution'
        }