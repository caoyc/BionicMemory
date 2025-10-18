"""Example demonstrating Newton cooling formula"""
import time
import math
import matplotlib.pyplot as plt
from typing import List, Tuple


def newton_cooling(
    initial_temp: float,
    ambient_temp: float,
    decay_rate: float,
    time_points: List[float]
) -> List[float]:
    """
    Calculate temperature decay using Newton's Law of Cooling.
    
    T(t) = T_ambient + (T_initial - T_ambient) * e^(-k*t)
    """
    temperatures = []
    for t in time_points:
        temp = ambient_temp + (initial_temp - ambient_temp) * math.exp(-decay_rate * t)
        temperatures.append(temp)
    return temperatures


def simulate_memory_decay():
    """Simulate memory decay with and without reinforcement"""
    
    # Time points (in arbitrary units, could be hours, days, etc.)
    time_points = list(range(0, 101))
    
    # Scenario 1: Natural decay (no access)
    natural_decay = newton_cooling(
        initial_temp=1.0,
        ambient_temp=0.0,
        decay_rate=0.05,  # Slower decay
        time_points=time_points
    )
    
    # Scenario 2: Memory with reinforcement
    reinforced_temps = []
    current_temp = 1.0
    
    for t in time_points:
        # Calculate decay since last point
        if t > 0:
            current_temp = 0.0 + (current_temp - 0.0) * math.exp(-0.05 * 1)
        
        # Simulate access/reinforcement at certain points
        if t in [20, 40, 60, 80]:
            current_temp = min(1.0, current_temp + 0.4)  # Boost on access
        
        reinforced_temps.append(current_temp)
    
    # Plot
    plt.figure(figsize=(12, 6))
    
    plt.subplot(1, 2, 1)
    plt.plot(time_points, natural_decay, 'b-', linewidth=2, label='Natural Decay')
    plt.axhline(y=0.01, color='r', linestyle='--', label='Forgetting Threshold')
    plt.xlabel('Time')
    plt.ylabel('Memory Temperature')
    plt.title('Ebbinghaus Forgetting Curve\n(Natural Decay)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.subplot(1, 2, 2)
    plt.plot(time_points, reinforced_temps, 'g-', linewidth=2, label='With Reinforcement')
    plt.axhline(y=0.01, color='r', linestyle='--', label='Forgetting Threshold')
    # Mark reinforcement points
    for t in [20, 40, 60, 80]:
        plt.axvline(x=t, color='orange', linestyle=':', alpha=0.5)
        plt.text(t, 0.9, '↑', fontsize=16, color='orange', ha='center')
    plt.xlabel('Time')
    plt.ylabel('Memory Temperature')
    plt.title('Memory with "Use it or Lose it"\n(Reinforcement at ↑)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/tmp/memory_decay_simulation.png', dpi=150, bbox_inches='tight')
    print("📊 Simulation saved to /tmp/memory_decay_simulation.png")
    
    # Print analysis
    print("\n📈 Memory Decay Analysis:")
    print(f"\nNatural Decay:")
    print(f"  - Time to reach threshold (0.01): ~{next((t for t, temp in zip(time_points, natural_decay) if temp < 0.01), 'never')} time units")
    print(f"  - Temperature after 50 time units: {natural_decay[50]:.4f}")
    
    print(f"\nWith Reinforcement:")
    print(f"  - Temperature after 50 time units: {reinforced_temps[50]:.4f}")
    print(f"  - Temperature at end: {reinforced_temps[-1]:.4f}")
    print(f"  - Memory remains 'hot' (>0.01) throughout the period!")


if __name__ == "__main__":
    print("🧠 BionicMemory: Newton Cooling Formula Demonstration\n")
    simulate_memory_decay()
