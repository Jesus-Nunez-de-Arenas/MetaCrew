"""
MMMU Benchmark Runner with Progress Monitoring
"""
import os
import time
import json
from datetime import datetime

def get_benchmark_status():
    """Check the current status of the benchmark"""
    output_dir = "./output_mmmu/"
    
    all_classes = [
        'Accounting', 'Agriculture', 'Architecture_and_Engineering', 'Art', 'Art_Theory',
        'Basic_Medical_Science', 'Biology', 'Chemistry', 'Clinical_Medicine', 'Computer_Science',
        'Design', 'Diagnostics_and_Laboratory_Medicine', 'Economics', 'Electronics', 'Energy_and_Power',
        'Finance', 'Geography', 'History', 'Literature', 'Manage', 'Marketing', 'Materials',
        'Math', 'Mechanical_Engineering', 'Music', 'Pharmacy', 'Physics', 'Psychology',
        'Public_Health', 'Sociology'
    ]
    
    total_completed = 0
    total_expected = 0
    
    print("📊 MMMU Benchmark Progress Report")
    print("=" * 60)
    print(f"{'Class':<30} {'Completed':<10} {'Progress':<10}")
    print("-" * 60)
    
    for cla in all_classes:
        result_file = f"{output_dir}/result_manual_crew_{cla}.jsonl"
        progress_file = f"{output_dir}/progress_manual_crew_{cla}.txt"
        
        completed = 0
        if os.path.exists(result_file):
            with open(result_file, 'r', encoding='utf-8') as f:
                completed = sum(1 for line in f if line.strip())
        
        # Estimate total samples (typically 30 per class in validation)
        expected = 30  # This is typical for MMMU validation sets
        
        progress_pct = (completed / expected * 100) if expected > 0 else 0
        
        status = "✅" if completed >= expected else "🔄" if completed > 0 else "⏳"
        
        print(f"{cla:<30} {completed:<10} {progress_pct:>6.1f}% {status}")
        
        total_completed += completed
        total_expected += expected
    
    print("-" * 60)
    overall_progress = (total_completed / total_expected * 100) if total_expected > 0 else 0
    print(f"{'TOTAL':<30} {total_completed:<10} {overall_progress:>6.1f}%")
    print("=" * 60)
    
    return total_completed, total_expected

def monitor_benchmark():
    """Monitor benchmark progress in real-time"""
    print("🔍 Starting benchmark monitoring...")
    print("Press Ctrl+C to stop monitoring\n")
    
    try:
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"⏰ Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            completed, total = get_benchmark_status()
            
            if completed >= total:
                print("\n🎉 BENCHMARK COMPLETED!")
                break
            
            print(f"\n⏳ Waiting 30 seconds before next update...")
            time.sleep(30)
            
    except KeyboardInterrupt:
        print("\n👋 Monitoring stopped by user")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "monitor":
        monitor_benchmark()
    else:
        get_benchmark_status()
