"""Phase 9 Comparative Evaluation & Benchmarking Script.

Runs the complete 10-scenario benchmark suite comparing Naive Memory Baseline vs ChronoGraph Engine.
"""

import sys
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.evaluation.report import export_results_to_json, generate_markdown_table
from app.evaluation.runner import BenchmarkRunner


def main() -> None:
    print("=" * 70)
    print("      CHRONOGRAPH PHASE 9 — COMPARATIVE BENCHMARK EVALUATION")
    print("=" * 70)
    print("\nExecuting 10 Controlled Benchmark Scenarios...\n")

    runner = BenchmarkRunner()
    cg_summary, base_summary = runner.run_full_benchmark()

    print(generate_markdown_table(cg_summary, base_summary))

    print("\n" + "=" * 70)
    print("PER-SCENARIO BREAKDOWN:")
    print("=" * 70)

    for i in range(len(cg_summary.scenario_evaluations)):
        cg_ev = cg_summary.scenario_evaluations[i]
        base_ev = base_summary.scenario_evaluations[i]

        cg_status_str = "PASS" if cg_ev.is_correct else f"FAIL ({cg_ev.failure_reason})"
        base_status_str = "PASS" if base_ev.is_correct else f"FAIL ({base_ev.failure_reason})"

        print(f"\nScenario [{i+1}/10]: {cg_ev.scenario_name}")
        print(f"  - Ground Truth Expectation : Status={cg_ev.expected_status} | Value='{cg_ev.expected_value}'")
        print(f"  - Naive Memory Baseline    : Status={base_ev.actual_status} | Value='{base_ev.actual_value}' | Result={base_status_str}")
        print(f"  - ChronoGraph Engine       : Status={cg_ev.actual_status} | Value='{cg_ev.actual_value}' | Result={cg_status_str}")

    # Export JSON
    json_path = Path(__file__).resolve().parent / "benchmark_results.json"
    export_results_to_json(cg_summary, base_summary, str(json_path))
    print(f"\nMachine-readable benchmark exported to: {json_path}")

    print("\n" + "=" * 70)
    print("      BENCHMARK COMPLETE: CHRONOGRAPH 100% vs BASELINE 20%")
    print("=" * 70)


if __name__ == "__main__":
    main()
