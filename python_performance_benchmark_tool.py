import time
import random
import statistics
import sys
import platform
import datetime
from typing import List, Tuple, Dict

class PerformanceBenchmark:
    """
    A class for conducting comprehensive performance benchmarks of various computations
    with extended test duration and reliable metrics
    """
    
    def __init__(self, seed: int = 42):
        """Initialize benchmark parameters and set random seed for reproducibility"""
        self.seed = seed
        random.seed(seed)
        self.results_history: List[Dict] = []
        
    # Matrix multiplication methods
    def generate_matrix(self, rows: int, cols: int) -> List[List[float]]:
        """Generate a matrix with random values between -1 and 1"""
        return [[random.uniform(-1, 1) for _ in range(cols)] 
                for _ in range(rows)]
    
    def matrix_multiply(self, 
                       matrix_a: List[List[float]], 
                       matrix_b: List[List[float]]) -> Tuple[List[List[float]], float]:
        """
        Perform matrix multiplication with precise timing measurement
        Returns: (result_matrix, execution_time)
        """
        if not matrix_a or not matrix_b or len(matrix_a[0]) != len(matrix_b):
            raise ValueError("Invalid matrix dimensions for multiplication")
        
        rows_a, cols_a = len(matrix_a), len(matrix_a[0])
        cols_b = len(matrix_b[0])
        
        # Initialize result matrix
        result = [[0.0] * cols_b for _ in range(rows_a)]
        
        # Measure execution time using high-precision counter
        start_time = time.perf_counter()
        
        # Perform multiplication
        for i in range(rows_a):
            for j in range(cols_b):
                for k in range(cols_a):
                    result[i][j] += matrix_a[i][k] * matrix_b[k][j]
                    
        execution_time = time.perf_counter() - start_time
        return result, execution_time
    
    def verify_accuracy(self):
        """Verify multiplication accuracy with a known test case"""
        print("\nVerifying multiplication accuracy...")
        test_a = [[1, 2], [3, 4]]
        test_b = [[5, 6], [7, 8]]
        expected = [[19, 22], [43, 50]]
        
        result, _ = self.matrix_multiply(test_a, test_b)
        
        is_correct = all(
            abs(result[i][j] - expected[i][j]) < 1e-10
            for i in range(len(result))
            for j in range(len(result[0]))
        )
        
        print("Verification result:", "PASSED" if is_correct else "FAILED")
        return is_correct
    
    def warm_up(self, size: int = 50):
        """Perform warm-up runs to stabilize performance"""
        print("Performing warm-up runs...")
        matrix_a = self.generate_matrix(size, size)
        matrix_b = self.generate_matrix(size, size)
        for _ in range(3):  # Perform 3 warm-up iterations
            self.matrix_multiply(matrix_a, matrix_b)
    
    def run_extended_benchmark(self, 
                             sizes: List[int], 
                             iterations: int = 5,
                             extended_runs: int = 3) -> Dict:
        """
        Run comprehensive matrix multiplication benchmark with multiple sizes and extended duration
        """
        benchmark_results = {}
        
        for size in sizes:
            print(f"\nBenchmarking {size}x{size} matrices...")
            size_results = []
            
            # Perform multiple extended runs
            for run in range(extended_runs):
                print(f"Extended run {run + 1}/{extended_runs}")
                run_times = []
                
                # Generate fresh matrices for each iteration
                for iter in range(iterations):
                    matrix_a = self.generate_matrix(size, size)
                    matrix_b = self.generate_matrix(size, size)
                    
                    # Perform multiplication and record time
                    _, execution_time = self.matrix_multiply(matrix_a, matrix_b)
                    run_times.append(execution_time)
                    
                    # Progress indicator
                    print(f"  Iteration {iter + 1}/{iterations}: {execution_time:.6f} seconds")
                
                size_results.extend(run_times)
            
            # Calculate comprehensive statistics
            total_ops_per_iter = size * size * size  # Assuming cubic complexity
            mean_time = statistics.mean(size_results)
            stats = {
                'size': size,
                'min_time': min(size_results),
                'max_time': max(size_results),
                'mean_time': mean_time,
                'median_time': statistics.median(size_results),
                'std_dev': statistics.stdev(size_results),
                'total_iterations': iterations * extended_runs,
                'total_operations': total_ops_per_iter * iterations * extended_runs,
                'operations_per_second': total_ops_per_iter / mean_time if mean_time > 0 else 0,
                'performance_score': 1 / statistics.median(size_results) if size_results else 0
            }
            benchmark_results[size] = stats
            self.results_history.append(stats)
            self._print_detailed_results(stats)
        
        return benchmark_results
    
    def _print_detailed_results(self, stats: Dict):
        """Print formatted benchmark results"""
        print("\nDetailed Performance Results")
        print("=" * 60)
        print(f"Matrix Size: {stats['size']}x{stats['size']}")
        print(f"Total Iterations: {stats['total_iterations']}")
        print("-" * 60)
        print(f"Minimum Time: {stats['min_time']:.6f} seconds")
        print(f"Maximum Time: {stats['max_time']:.6f} seconds")
        print(f"Mean Time: {stats['mean_time']:.6f} seconds")
        print(f"Median Time: {stats['median_time']:.6f} seconds")
        print(f"Standard Deviation: {stats['std_dev']:.6f} seconds")
        print(f"Operations per Second: {stats['operations_per_second']:,.2f}")
        print(f"Performance Score: {stats['performance_score']:,.2f}")
        print("=" * 60)
    
    # New method for recursive Fibonacci calculation
    def recursive_fibonacci(self, n: int) -> int:
        """Calculate the nth Fibonacci number recursively"""
        if n <= 0:
            raise ValueError("n must be a positive integer")
        if n == 1 or n == 2:
            return 1
        return self.recursive_fibonacci(n - 1) + self.recursive_fibonacci(n - 2)
    
    def run_fibonacci_benchmark(self, n_values: List[int]) -> Dict:
        """
        Run benchmark on recursive Fibonacci calculation for given n values
        """
        print("\nStarting Fibonacci benchmark...")
        benchmark_results = {}
    
        for n in n_values:
            print(f"\nCalculating Fibonacci number for n={n}")
            times = []
            # Limit recursion depth to prevent RecursionError
            sys.setrecursionlimit(max(1000, n + 10))
            try:
                start_time = time.perf_counter()
                result = self.recursive_fibonacci(n)
                execution_time = time.perf_counter() - start_time
                times.append(execution_time)
                print(f"  Result: Fib({n}) = {result}")
                print(f"  Time taken: {execution_time:.6f} seconds")
                
                performance_score = 1 / execution_time if execution_time > 0 else 0
                
                stats = {
                    'n': n,
                    'execution_time': execution_time,
                    'performance_score': performance_score
                }
                benchmark_results[n] = stats
                self.results_history.append(stats)
    
            except RecursionError:
                print(f"  RecursionError: Maximum recursion depth exceeded for n={n}")
                benchmark_results[n] = {'n': n, 'execution_time': None, 'performance_score': 0}
            
        return benchmark_results
    
    # New method for bubble sort
    def bubble_sort(self, data: List[int]) -> Tuple[List[int], float]:
        """Sort the list using bubble sort and measure time"""
        n = len(data)
        data_copy = data.copy()
        start_time = time.perf_counter()
        for i in range(n):
            for j in range(0, n - i - 1):
                if data_copy[j] > data_copy[j + 1]:
                    data_copy[j], data_copy[j + 1] = data_copy[j + 1], data_copy[j]
        execution_time = time.perf_counter() - start_time
        return data_copy, execution_time
    
    def run_sort_benchmark(self, list_sizes: List[int]) -> Dict:
        """
        Run benchmark on bubble sort for lists of different sizes
        """
        print("\nStarting Bubble Sort benchmark...")
        benchmark_results = {}
    
        for size in list_sizes:
            print(f"\nSorting list of size {size}")
            data = [random.randint(-1000, 1000) for _ in range(size)]
            sorted_data, execution_time = self.bubble_sort(data)
            print(f"  Time taken: {execution_time:.6f} seconds")
            
            performance_score = 1 / execution_time if execution_time > 0 else 0
            
            stats = {
                'size': size,
                'execution_time': execution_time,
                'performance_score': performance_score
            }
            benchmark_results[size] = stats
            self.results_history.append(stats)
        
        return benchmark_results
    
    # New method for unoptimized sieve of Eratosthenes
    def unoptimized_sieve(self, limit: int) -> Tuple[List[int], float]:
        """Generate primes up to limit using an unoptimized sieve and measure time"""
        start_time = time.perf_counter()
        primes = []
        for num in range(2, limit + 1):
            is_prime = True
            for i in range(2, num):
                if num % i == 0:
                    is_prime = False
                    break
            if is_prime:
                primes.append(num)
        execution_time = time.perf_counter() - start_time
        return primes, execution_time
    
    def run_sieve_benchmark(self, limits: List[int]) -> Dict:
        """
        Run benchmark on unoptimized prime number generation
        """
        print("\nStarting Prime Number Generation benchmark...")
        benchmark_results = {}
    
        for limit in limits:
            print(f"\nGenerating primes up to {limit}")
            primes, execution_time = self.unoptimized_sieve(limit)
            print(f"  Primes found: {len(primes)}")
            print(f"  Time taken: {execution_time:.6f} seconds")
            
            performance_score = 1 / execution_time if execution_time > 0 else 0
            
            stats = {
                'limit': limit,
                'execution_time': execution_time,
                'primes_found': len(primes),
                'performance_score': performance_score
            }
            benchmark_results[limit] = stats
            self.results_history.append(stats)
        
        return benchmark_results

def main():
    print("Python Performance Benchmark Tool")
    print("Version: 1.1")
    print("Author: Alpha Beta Network Research Team")
    print("(c) 2024 Alpha Beta Network (alphabetanet.com) All Rights Reserved.")
    print("-------------------------------------------------------------------")	
    # Collect system information
    os_name = platform.system()
    os_version = platform.version()
    architecture = platform.architecture()[0]
    processor = platform.processor()
    python_version = sys.version.replace('\n', ' ')
    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Open log file
    with open('python_performance_benchmark.log', 'a') as logfile:
        def print_and_log(s):
            print(s)
            logfile.write(s + '\n')
        
        # Output system information
        print_and_log(f"Date of testing: {current_date}")
        print_and_log("System Information")
        print_and_log("=" * 60)
        print_and_log(f"Operating System: {os_name} ({architecture})")
        print_and_log(f"Processor: {processor}")
        print_and_log(f"Python Version: {python_version}")
        print_and_log("=" * 60)
        
        # Initialize benchmark
        benchmark = PerformanceBenchmark(seed=42)
        
        # Verify multiplication accuracy
        if not benchmark.verify_accuracy():
            print_and_log("ERROR: Matrix multiplication verification failed!")
            return
        
        # Perform warm-up
        benchmark.warm_up()
        
        # Define test parameters for matrix multiplication
        matrix_sizes = [200]
        iterations_per_size = 5
        extended_runs = 3
        
        # Run comprehensive matrix multiplication benchmark
        print_and_log("\nStarting benchmark...")
        matrix_results = benchmark.run_extended_benchmark(
            sizes=matrix_sizes,
            iterations=iterations_per_size,
            extended_runs=extended_runs
        )
    
        # Define test parameters for Fibonacci benchmark
        fibonacci_n_values = [35]  # Adjust n for reasonable execution times
    
        # Run Fibonacci benchmark
        fibonacci_results = benchmark.run_fibonacci_benchmark(fibonacci_n_values)
    
        # Define test parameters for Bubble Sort benchmark
        sort_list_sizes = [5000]  # Small sizes due to inefficiency of bubble sort
    
        # Run Bubble Sort benchmark
        sort_results = benchmark.run_sort_benchmark(sort_list_sizes)
    
        # Define test parameters for Prime Number Generation benchmark
        sieve_limits = [30000]  # Adjust limits for reasonable execution times
    
        # Run Prime Number Generation benchmark
        sieve_results = benchmark.run_sieve_benchmark(sieve_limits)
        
        # Print summary
        print_and_log("\nBenchmark Summary")
        print_and_log("=" * 60)
        
        # Matrix multiplication summary
        print_and_log("\nMatrix Multiplication Results:")
        for size, stats in matrix_results.items():
            print_and_log(f"Size {size}x{size}:")
            print_and_log(f"  Median time: {stats['median_time']:.6f} seconds")
            print_and_log(f"  Operations/second: {stats['operations_per_second']:,.2f}")
            print_and_log(f"  Coefficient of variation: {(stats['std_dev']/stats['mean_time'])*100:.2f}%")
            print_and_log(f"  Performance Score: {stats['performance_score']:,.2f}")
        
        # Fibonacci benchmark summary
        print_and_log("\nRecursive Fibonacci Results:")
        for n, stats in fibonacci_results.items():
            print_and_log(f"n={n}:")
            if stats['execution_time'] is not None:
                print_and_log(f"  Time taken: {stats['execution_time']:.6f} seconds")
                print_and_log(f"  Performance Score: {stats['performance_score']:.2f}")
            else:
                print_and_log(f"  Calculation failed due to recursion depth limit.")
        
        # Bubble Sort benchmark summary
        print_and_log("\nBubble Sort Results:")
        for size, stats in sort_results.items():
            print_and_log(f"List size {size}:")
            print_and_log(f"  Time taken: {stats['execution_time']:.6f} seconds")
            print_and_log(f"  Performance Score: {stats['performance_score']:.2f}")
        
        # Prime Number Generation benchmark summary
        print_and_log("\nPrime Number Generation Results:")
        for limit, stats in sieve_results.items():
            print_and_log(f"Limit {limit}:")
            print_and_log(f"  Primes found: {stats['primes_found']}")
            print_and_log(f"  Time taken: {stats['execution_time']:.6f} seconds")
            print_and_log(f"  Performance Score: {stats['performance_score']:.2f}")
        
        # Compute Summary Evaluation
        total_performance_score = 0

        # Matrix Multiplication performance scores
        for size, stats in matrix_results.items():
            total_performance_score += stats.get('performance_score', 0)

        # Fibonacci performance scores
        for n, stats in fibonacci_results.items():
            if stats.get('execution_time'):
                total_performance_score += stats.get('performance_score', 0)

        # Bubble Sort performance scores
        for size, stats in sort_results.items():
            total_performance_score += stats.get('performance_score', 0)

        # Sieve performance scores
        for limit, stats in sieve_results.items():
            total_performance_score += stats.get('performance_score', 0)

        print_and_log(f"\nSummary Evaluation (Higher is better): {total_performance_score:.6f}")
        
        # Add informational message about performance optimization
        optimization_message = """
---
Note: To improve your Python code performance by 60-100%, you can utilize the 
"Python Binary Optimization Compiler Script" from Alpha Beta Network (alphabetanet.com)

"""
        print_and_log(optimization_message)

if __name__ == "__main__":
    main()