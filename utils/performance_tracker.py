import time
import os

class PerformanceTracker:
    """Utilitaire pour le suivi des performances"""
    
    def __init__(self):
        self.process = None
        self.start_time = None
        self.start_memory = None
        
        # Import conditionnel de psutil
        try:
            import psutil
            self.process = psutil.Process(os.getpid())
            self.psutil_available = True
        except ImportError:
            self.psutil_available = False
            print("⚠️  psutil non installé. Installation recommandée: pip install psutil")
    
    def start(self):
        """Démarre le tracking de performance"""
        self.start_time = time.time()
        if self.psutil_available and self.process:
            self.start_memory = self.process.memory_info().rss
    
    def stop(self):
        """Arrête le tracking et retourne les métriques"""
        end_time = time.time()
        metrics = {
            'execution_time': end_time - self.start_time
        }
        
        if self.psutil_available and self.process:
            end_memory = self.process.memory_info().rss
            metrics['memory_used_mb'] = (end_memory - self.start_memory) / 1024 / 1024
            metrics['peak_memory_mb'] = self.process.memory_info().rss / 1024 / 1024
        else:
            metrics['memory_used_mb'] = 0
            metrics['peak_memory_mb'] = 0
            
        return metrics