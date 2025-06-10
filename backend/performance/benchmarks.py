"""
AI-RPG-Alpha: Performance Benchmarks

Performance benchmarking and optimization tools for the AI-RPG system.
Includes system profiling, bottleneck identification, and optimization recommendations.
Part of Phase 5: Testing & Optimization as defined in PRD.
"""

import asyncio
import time
import psutil
import gc
import tracemalloc
import statistics
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from pathlib import Path
import json
import sqlite3
import tempfile
import shutil
from concurrent.futures import ThreadPoolExecutor

from backend.dao.game_state import GameStateDAO
from backend.dao.memory import MemoryDAO
from backend.engine.consequence import ConsequenceEngine
from backend.engine.combat import CombatResolver
from backend.ai.openai_client import OpenAIClient
from backend.models.dataclasses import Player, Quest, MemoryEntry, GameEvent


@dataclass
class BenchmarkResult:
    """Results from a performance benchmark"""
    name: str
    duration: float
    memory_peak: int
    memory_current: int
    cpu_percent: float
    operations_per_second: float
    success_rate: float
    error_count: int
    metadata: Dict[str, Any]


@dataclass
class SystemMetrics:
    """System-wide performance metrics"""
    timestamp: float
    cpu_percent: float
    memory_percent: float
    memory_available: int
    disk_io_read: int
    disk_io_write: int
    network_io_sent: int
    network_io_recv: int


class PerformanceProfiler:
    """Performance profiler for AI-RPG system components"""
    
    def __init__(self):
        self.results: List[BenchmarkResult] = []
        self.system_metrics: List[SystemMetrics] = []
        self.profiling_active = False
    
    def start_profiling(self):
        """Start system-wide performance profiling"""
        self.profiling_active = True
        tracemalloc.start()
        gc.collect()  # Clean start
    
    def stop_profiling(self):
        """Stop performance profiling"""
        self.profiling_active = False
        tracemalloc.stop()
    
    async def benchmark_function(
        self, 
        func: Callable, 
        name: str, 
        iterations: int = 100,
        *args, 
        **kwargs
    ) -> BenchmarkResult:
        """Benchmark a specific function"""
        
        # Collect initial metrics
        gc.collect()
        process = psutil.Process()
        initial_memory = process.memory_info().rss
        
        # Record system state
        if tracemalloc.is_tracing():
            snapshot_start = tracemalloc.take_snapshot()
        
        start_time = time.time()
        error_count = 0
        successful_operations = 0
        
        # Run benchmark iterations
        for i in range(iterations):
            try:
                if asyncio.iscoroutinefunction(func):
                    await func(*args, **kwargs)
                else:
                    func(*args, **kwargs)
                successful_operations += 1
            except Exception as e:
                error_count += 1
                print(f"Error in iteration {i}: {e}")
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Collect final metrics
        final_memory = process.memory_info().rss
        cpu_percent = process.cpu_percent()
        
        if tracemalloc.is_tracing():
            snapshot_end = tracemalloc.take_snapshot()
            memory_peak = snapshot_end.compare_to(snapshot_start, 'lineno')[0].size_diff
        else:
            memory_peak = final_memory - initial_memory
        
        # Calculate metrics
        operations_per_second = successful_operations / duration if duration > 0 else 0
        success_rate = successful_operations / iterations if iterations > 0 else 0
        
        result = BenchmarkResult(
            name=name,
            duration=duration,
            memory_peak=memory_peak,
            memory_current=final_memory,
            cpu_percent=cpu_percent,
            operations_per_second=operations_per_second,
            success_rate=success_rate,
            error_count=error_count,
            metadata={
                "iterations": iterations,
                "avg_time_per_operation": duration / iterations if iterations > 0 else 0
            }
        )
        
        self.results.append(result)
        return result
    
    def collect_system_metrics(self) -> SystemMetrics:
        """Collect current system metrics"""
        cpu_percent = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        disk_io = psutil.disk_io_counters()
        network_io = psutil.net_io_counters()
        
        metrics = SystemMetrics(
            timestamp=time.time(),
            cpu_percent=cpu_percent,
            memory_percent=memory.percent,
            memory_available=memory.available,
            disk_io_read=disk_io.read_bytes if disk_io else 0,
            disk_io_write=disk_io.write_bytes if disk_io else 0,
            network_io_sent=network_io.bytes_sent if network_io else 0,
            network_io_recv=network_io.bytes_recv if network_io else 0
        )
        
        self.system_metrics.append(metrics)
        return metrics
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report"""
        if not self.results:
            return {"error": "No benchmark results available"}
        
        # Aggregate results
        total_duration = sum(r.duration for r in self.results)
        avg_ops_per_second = statistics.mean(r.operations_per_second for r in self.results)
        avg_success_rate = statistics.mean(r.success_rate for r in self.results)
        total_errors = sum(r.error_count for r in self.results)
        
        # Find bottlenecks
        slowest_operation = min(self.results, key=lambda r: r.operations_per_second)
        highest_memory_usage = max(self.results, key=lambda r: r.memory_peak)
        
        return {
            "summary": {
                "total_benchmarks": len(self.results),
                "total_duration": total_duration,
                "average_ops_per_second": avg_ops_per_second,
                "average_success_rate": avg_success_rate,
                "total_errors": total_errors
            },
            "bottlenecks": {
                "slowest_operation": {
                    "name": slowest_operation.name,
                    "ops_per_second": slowest_operation.operations_per_second
                },
                "highest_memory_usage": {
                    "name": highest_memory_usage.name,
                    "memory_peak": highest_memory_usage.memory_peak
                }
            },
            "detailed_results": [
                {
                    "name": r.name,
                    "duration": r.duration,
                    "ops_per_second": r.operations_per_second,
                    "success_rate": r.success_rate,
                    "memory_peak": r.memory_peak,
                    "error_count": r.error_count
                }
                for r in self.results
            ]
        }


class DatabaseBenchmarks:
    """Database performance benchmarks"""
    
    def __init__(self):
        self.profiler = PerformanceProfiler()
    
    async def benchmark_sqlite_operations(self, iterations: int = 1000) -> Dict[str, BenchmarkResult]:
        """Benchmark SQLite database operations"""
        results = {}
        
        # Setup temporary database
        temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        temp_db.close()
        
        try:
            game_dao = GameStateDAO(db_path=temp_db.name)
            
            # Benchmark player creation
            async def create_player():
                player = Player(
                    name=f"BenchPlayer{time.time()}",
                    level=1,
                    experience=0,
                    health=50,
                    max_health=50
                )
                return await game_dao.create_player(player)
            
            results["player_creation"] = await self.profiler.benchmark_function(
                create_player, "Player Creation", iterations=iterations
            )
            
            # Create sample players for read benchmarks
            sample_players = []
            for i in range(100):
                player = await create_player()
                sample_players.append(player)
            
            # Benchmark player retrieval
            async def get_player():
                player_id = sample_players[hash(time.time()) % len(sample_players)].id
                return await game_dao.get_player_by_id(player_id)
            
            results["player_retrieval"] = await self.profiler.benchmark_function(
                get_player, "Player Retrieval", iterations=iterations
            )
            
            # Benchmark player updates
            async def update_player():
                player = sample_players[hash(time.time()) % len(sample_players)]
                player.experience += 10
                return await game_dao.update_player(player)
            
            results["player_update"] = await self.profiler.benchmark_function(
                update_player, "Player Update", iterations=iterations//10
            )
            
            # Benchmark quest operations
            async def create_quest():
                player = sample_players[hash(time.time()) % len(sample_players)]
                quest = Quest(
                    player_id=player.id,
                    title=f"Benchmark Quest {time.time()}",
                    description="A test quest for benchmarking",
                    objectives=["Complete benchmark"],
                    rewards={"experience": 50}
                )
                return await game_dao.create_quest(quest)
            
            results["quest_creation"] = await self.profiler.benchmark_function(
                create_quest, "Quest Creation", iterations=iterations//5
            )
            
        finally:
            Path(temp_db.name).unlink(missing_ok=True)
        
        return results
    
    async def benchmark_chromadb_operations(self, iterations: int = 500) -> Dict[str, BenchmarkResult]:
        """Benchmark ChromaDB vector operations"""
        results = {}
        
        # Setup temporary ChromaDB
        temp_dir = tempfile.mkdtemp()
        
        try:
            memory_dao = MemoryDAO(db_path=temp_dir)
            
            # Benchmark memory storage
            async def store_memory():
                memory = MemoryEntry(
                    id=f"bench_memory_{time.time()}_{hash(time.time()) % 10000}",
                    player_id="benchmark_player",
                    content=f"Benchmark memory content {time.time()}",
                    memory_type="benchmark",
                    importance=0.5,
                    context_tags=["benchmark", "test"],
                    location="test_location",
                    timestamp=int(time.time())
                )
                return await memory_dao.store_memory(memory)
            
            results["memory_storage"] = await self.profiler.benchmark_function(
                store_memory, "Memory Storage", iterations=iterations
            )
            
            # Store sample memories for search benchmarks
            for i in range(50):
                await store_memory()
            
            # Benchmark memory search
            async def search_memories():
                return await memory_dao.search_similar_memories(
                    player_id="benchmark_player",
                    query="benchmark test content",
                    limit=10
                )
            
            results["memory_search"] = await self.profiler.benchmark_function(
                search_memories, "Memory Search", iterations=iterations//5
            )
            
            # Benchmark memory retrieval
            async def get_memories():
                return await memory_dao.get_memories_by_player("benchmark_player")
            
            results["memory_retrieval"] = await self.profiler.benchmark_function(
                get_memories, "Memory Retrieval", iterations=iterations//2
            )
            
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)
        
        return results


class EngineBenchmarks:
    """Game engine performance benchmarks"""
    
    def __init__(self):
        self.profiler = PerformanceProfiler()
    
    async def benchmark_consequence_engine(self, iterations: int = 200) -> Dict[str, BenchmarkResult]:
        """Benchmark consequence engine performance"""
        results = {}
        
        # Setup temporary databases
        temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        temp_db.close()
        temp_chromadb = tempfile.mkdtemp()
        
        try:
            game_dao = GameStateDAO(db_path=temp_db.name)
            memory_dao = MemoryDAO(db_path=temp_chromadb)
            consequence_engine = ConsequenceEngine(
                game_state_dao=game_dao,
                memory_dao=memory_dao
            )
            
            # Create test player
            player = Player(
                name="ConsequenceBenchPlayer",
                level=3,
                experience=100,
                health=75,
                max_health=100
            )
            test_player = await game_dao.create_player(player)
            
            # Benchmark consequence registration
            from backend.models.dataclasses import Consequence
            from backend.engine.consequence_types import ConsequenceType, ConsequenceImpact
            
            async def register_consequence():
                consequence = Consequence(
                    id=f"bench_consequence_{time.time()}_{hash(time.time()) % 10000}",
                    player_id=test_player.id,
                    consequence_type=ConsequenceType.DELAYED_EVENT,
                    trigger_event="benchmark_event",
                    impact=ConsequenceImpact.MEDIUM,
                    description="Benchmark consequence",
                    delay_turns=3
                )
                return await consequence_engine.register_consequence(consequence)
            
            results["consequence_registration"] = await self.profiler.benchmark_function(
                register_consequence, "Consequence Registration", iterations=iterations
            )
            
            # Benchmark turn processing
            async def process_turn():
                return await consequence_engine.process_turn(test_player.id, hash(time.time()) % 10)
            
            results["turn_processing"] = await self.profiler.benchmark_function(
                process_turn, "Turn Processing", iterations=iterations//2
            )
            
        finally:
            Path(temp_db.name).unlink(missing_ok=True)
            shutil.rmtree(temp_chromadb, ignore_errors=True)
        
        return results
    
    async def benchmark_combat_system(self, iterations: int = 100) -> Dict[str, BenchmarkResult]:
        """Benchmark combat system performance"""
        results = {}
        
        # Mock AI client for faster testing
        from unittest.mock import Mock, AsyncMock
        mock_ai_client = Mock()
        mock_ai_client.generate_narrative = AsyncMock(return_value={
            "narrative": "Combat benchmark result",
            "damage_dealt": 10,
            "damage_taken": 5,
            "combat_ended": True,
            "victory": True
        })
        
        from backend.engine.risk_assessment import RiskAssessment
        risk_assessment = RiskAssessment()
        
        combat_resolver = CombatResolver(
            ai_client=mock_ai_client,
            risk_assessment=risk_assessment
        )
        
        # Create test characters
        player = Player(
            id="combat_bench_player",
            name="CombatBenchPlayer",
            level=5,
            experience=200,
            health=100,
            max_health=100,
            stats={
                "strength": 15,
                "dexterity": 12,
                "constitution": 14,
                "intelligence": 10,
                "wisdom": 11,
                "charisma": 9
            }
        )
        
        from backend.models.dataclasses import Enemy
        enemy = Enemy(
            id="combat_bench_enemy",
            name="Benchmark Enemy",
            level=4,
            health=50,
            max_health=50,
            stats={
                "strength": 12,
                "dexterity": 10,
                "constitution": 12
            }
        )
        
        # Benchmark combat initiation
        async def initiate_combat():
            return await combat_resolver.initiate_combat(player, enemy, "benchmark")
        
        results["combat_initiation"] = await self.profiler.benchmark_function(
            initiate_combat, "Combat Initiation", iterations=iterations
        )
        
        # Benchmark combat resolution
        from backend.models.dataclasses import CombatAction
        action = CombatAction(type="attack", target="enemy", weapon="sword")
        
        async def resolve_combat_action():
            return await combat_resolver.resolve_action(player, enemy, action)
        
        results["combat_resolution"] = await self.profiler.benchmark_function(
            resolve_combat_action, "Combat Resolution", iterations=iterations
        )
        
        return results


class AIBenchmarks:
    """AI service performance benchmarks"""
    
    def __init__(self):
        self.profiler = PerformanceProfiler()
    
    async def benchmark_ai_responses(self, iterations: int = 20) -> Dict[str, BenchmarkResult]:
        """Benchmark AI response generation (uses mock to avoid API costs)"""
        results = {}
        
        # Mock AI client to simulate response times
        from unittest.mock import Mock, AsyncMock
        import random
        
        mock_ai_client = Mock()
        
        async def mock_generate_quest(*args, **kwargs):
            # Simulate AI processing time
            await asyncio.sleep(random.uniform(0.1, 0.5))
            return {
                "title": "Mock Quest",
                "description": "A mock quest for benchmarking",
                "objectives": ["Mock objective"],
                "rewards": {"experience": 50}
            }
        
        async def mock_generate_choice_result(*args, **kwargs):
            # Simulate AI processing time
            await asyncio.sleep(random.uniform(0.05, 0.3))
            return {
                "result": "Mock choice result",
                "consequences": {"experience": 10}
            }
        
        mock_ai_client.generate_quest = mock_generate_quest
        mock_ai_client.generate_choice_result = mock_generate_choice_result
        
        # Benchmark quest generation
        results["quest_generation"] = await self.profiler.benchmark_function(
            mock_ai_client.generate_quest, "Quest Generation", iterations=iterations
        )
        
        # Benchmark choice result generation
        results["choice_generation"] = await self.profiler.benchmark_function(
            mock_ai_client.generate_choice_result, "Choice Generation", iterations=iterations
        )
        
        return results


class ConcurrencyBenchmarks:
    """Concurrency and load testing benchmarks"""
    
    def __init__(self):
        self.profiler = PerformanceProfiler()
    
    async def benchmark_concurrent_operations(self, concurrent_users: int = 50) -> Dict[str, BenchmarkResult]:
        """Benchmark system under concurrent load"""
        results = {}
        
        # Setup test environment
        temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        temp_db.close()
        temp_chromadb = tempfile.mkdtemp()
        
        try:
            game_dao = GameStateDAO(db_path=temp_db.name)
            memory_dao = MemoryDAO(db_path=temp_chromadb)
            
            # Benchmark concurrent player creation
            async def concurrent_player_creation():
                tasks = []
                for i in range(concurrent_users):
                    async def create_user_player():
                        player = Player(
                            name=f"ConcurrentPlayer{i}_{time.time()}",
                            level=1,
                            experience=0,
                            health=50,
                            max_health=50
                        )
                        return await game_dao.create_player(player)
                    tasks.append(create_user_player())
                
                return await asyncio.gather(*tasks)
            
            start_time = time.time()
            concurrent_results = await concurrent_player_creation()
            duration = time.time() - start_time
            
            success_rate = len([r for r in concurrent_results if r is not None]) / concurrent_users
            
            results["concurrent_creation"] = BenchmarkResult(
                name="Concurrent Player Creation",
                duration=duration,
                memory_peak=0,  # Not measured in this context
                memory_current=0,
                cpu_percent=0,
                operations_per_second=concurrent_users / duration,
                success_rate=success_rate,
                error_count=concurrent_users - len([r for r in concurrent_results if r is not None]),
                metadata={"concurrent_users": concurrent_users}
            )
            
            # Benchmark concurrent memory operations
            players = [r for r in concurrent_results if r is not None][:10]  # Use first 10 players
            
            async def concurrent_memory_operations():
                tasks = []
                for i, player in enumerate(players):
                    async def store_player_memory():
                        memory = MemoryEntry(
                            id=f"concurrent_memory_{player.id}_{time.time()}",
                            player_id=player.id,
                            content=f"Concurrent memory for {player.name}",
                            memory_type="concurrent_test",
                            importance=0.5,
                            context_tags=["concurrent", "benchmark"],
                            location="test_location",
                            timestamp=int(time.time())
                        )
                        return await memory_dao.store_memory(memory)
                    tasks.append(store_player_memory())
                
                return await asyncio.gather(*tasks)
            
            start_time = time.time()
            memory_results = await concurrent_memory_operations()
            duration = time.time() - start_time
            
            success_rate = len([r for r in memory_results if r is True]) / len(players)
            
            results["concurrent_memory"] = BenchmarkResult(
                name="Concurrent Memory Operations",
                duration=duration,
                memory_peak=0,
                memory_current=0,
                cpu_percent=0,
                operations_per_second=len(players) / duration,
                success_rate=success_rate,
                error_count=len(players) - len([r for r in memory_results if r is True]),
                metadata={"concurrent_operations": len(players)}
            )
            
        finally:
            Path(temp_db.name).unlink(missing_ok=True)
            shutil.rmtree(temp_chromadb, ignore_errors=True)
        
        return results


class BenchmarkRunner:
    """Main benchmark runner and coordinator"""
    
    def __init__(self):
        self.profiler = PerformanceProfiler()
        self.db_benchmarks = DatabaseBenchmarks()
        self.engine_benchmarks = EngineBenchmarks()
        self.ai_benchmarks = AIBenchmarks()
        self.concurrency_benchmarks = ConcurrencyBenchmarks()
    
    async def run_all_benchmarks(self, iterations: int = 100) -> Dict[str, Any]:
        """Run comprehensive benchmark suite"""
        print("🚀 Starting AI-RPG Performance Benchmark Suite...")
        
        all_results = {}
        
        self.profiler.start_profiling()
        
        try:
            # Database benchmarks
            print("📊 Running database benchmarks...")
            db_results = await self.db_benchmarks.benchmark_sqlite_operations(iterations)
            chromadb_results = await self.db_benchmarks.benchmark_chromadb_operations(iterations//2)
            all_results["database"] = {**db_results, **chromadb_results}
            
            # Engine benchmarks
            print("⚙️ Running engine benchmarks...")
            consequence_results = await self.engine_benchmarks.benchmark_consequence_engine(iterations//5)
            combat_results = await self.engine_benchmarks.benchmark_combat_system(iterations//10)
            all_results["engine"] = {**consequence_results, **combat_results}
            
            # AI benchmarks
            print("🤖 Running AI benchmarks...")
            ai_results = await self.ai_benchmarks.benchmark_ai_responses(iterations//50)
            all_results["ai"] = ai_results
            
            # Concurrency benchmarks
            print("🔄 Running concurrency benchmarks...")
            concurrency_results = await self.concurrency_benchmarks.benchmark_concurrent_operations(25)
            all_results["concurrency"] = concurrency_results
            
        finally:
            self.profiler.stop_profiling()
        
        # Generate comprehensive report
        performance_report = self.profiler.get_performance_report()
        
        final_report = {
            "timestamp": time.time(),
            "system_info": {
                "cpu_count": psutil.cpu_count(),
                "memory_total": psutil.virtual_memory().total,
                "python_version": f"{psutil.LINUX if hasattr(psutil, 'LINUX') else 'Unknown'}"
            },
            "benchmark_results": all_results,
            "performance_summary": performance_report,
            "recommendations": self.generate_optimization_recommendations(all_results)
        }
        
        return final_report
    
    def generate_optimization_recommendations(self, results: Dict[str, Any]) -> List[str]:
        """Generate optimization recommendations based on benchmark results"""
        recommendations = []
        
        # Analyze database performance
        if "database" in results:
            db_results = results["database"]
            
            if "player_creation" in db_results:
                create_result = db_results["player_creation"]
                if create_result.operations_per_second < 100:
                    recommendations.append(
                        "Consider optimizing player creation queries or adding database indexing"
                    )
            
            if "memory_storage" in db_results:
                memory_result = db_results["memory_storage"]
                if memory_result.operations_per_second < 50:
                    recommendations.append(
                        "ChromaDB vector storage performance could be improved with batch operations"
                    )
        
        # Analyze engine performance
        if "engine" in results:
            engine_results = results["engine"]
            
            if "consequence_registration" in engine_results:
                consequence_result = engine_results["consequence_registration"]
                if consequence_result.memory_peak > 50 * 1024 * 1024:  # 50MB
                    recommendations.append(
                        "Consequence engine memory usage is high - consider implementing memory pooling"
                    )
        
        # Analyze concurrency performance
        if "concurrency" in results:
            concurrency_results = results["concurrency"]
            
            for result_name, result in concurrency_results.items():
                if result.success_rate < 0.95:
                    recommendations.append(
                        f"Concurrency issue detected in {result_name} - review thread safety"
                    )
        
        # General recommendations
        recommendations.extend([
            "Consider implementing connection pooling for database operations",
            "Add caching layer for frequently accessed data",
            "Implement async batch processing for bulk operations",
            "Monitor memory usage in production and set up alerts",
            "Consider horizontal scaling for increased load"
        ])
        
        return recommendations
    
    def save_report(self, report: Dict[str, Any], filename: str = None):
        """Save benchmark report to file"""
        if filename is None:
            timestamp = int(time.time())
            filename = f"performance_report_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"📄 Performance report saved to {filename}")


async def main():
    """Main function to run performance benchmarks"""
    runner = BenchmarkRunner()
    
    print("🔧 AI-RPG Alpha Performance Benchmark Suite")
    print("=" * 50)
    
    # Run benchmarks with different iteration counts based on component
    report = await runner.run_all_benchmarks(iterations=100)
    
    # Save report
    runner.save_report(report)
    
    # Print summary
    print("\n📈 Benchmark Summary:")
    print("-" * 30)
    
    if "performance_summary" in report:
        summary = report["performance_summary"]["summary"]
        print(f"Total benchmarks: {summary['total_benchmarks']}")
        print(f"Total duration: {summary['total_duration']:.2f}s")
        print(f"Average ops/sec: {summary['average_ops_per_second']:.2f}")
        print(f"Success rate: {summary['average_success_rate']:.2%}")
    
    if "recommendations" in report:
        print("\n💡 Optimization Recommendations:")
        for i, rec in enumerate(report["recommendations"][:5], 1):
            print(f"{i}. {rec}")
    
    print("\n✅ Benchmark suite completed!")


if __name__ == "__main__":
    asyncio.run(main()) 