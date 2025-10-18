"""Visual demonstration of memory decay and reinforcement"""
import time
import math


def print_temperature_bar(temp, width=40):
    """Print a visual bar representing temperature"""
    filled = int(temp * width)
    bar = "█" * filled + "░" * (width - filled)
    
    if temp > 0.7:
        icon = "🔥"
        color = ""
    elif temp > 0.3:
        icon = "🌡️"
        color = ""
    else:
        icon = "❄️"
        color = ""
    
    return f"{icon} [{bar}] {temp:.2f}"


def simulate_memory_lifecycle():
    """Simulate a memory's lifecycle with visual output"""
    print("\n" + "=" * 70)
    print("BionicMemory: Memory Lifecycle Simulation")
    print("=" * 70)
    
    print("\n📝 Creating a new memory: 'Python is a great programming language'")
    print("   Initial temperature: 1.00 (Fresh memory)")
    
    temperature = 1.0
    decay_rate = 0.15
    ambient_temp = 0.0
    threshold = 0.01
    
    print(f"\n{print_temperature_bar(temperature)}")
    
    # Phase 1: Natural decay
    print("\n⏰ Phase 1: Natural decay (no access)")
    print("   Memory gradually cools down over time...")
    
    time_steps = [2, 5, 10, 15, 20]
    total_time = 0
    
    for t in time_steps:
        time_delta = t - total_time
        total_time = t
        
        # Apply Newton cooling
        temperature = ambient_temp + (temperature - ambient_temp) * math.exp(-decay_rate * time_delta)
        
        print(f"   After {total_time:2d}s: {print_temperature_bar(temperature)}")
        
        if temperature < threshold:
            print(f"\n   ⚠️  Memory temperature dropped below threshold ({threshold})")
            print(f"   💀 Memory would be forgotten!")
            break
    
    # Phase 2: Reinforcement
    if temperature >= threshold:
        print(f"\n⏰ Phase 2: Memory access and reinforcement")
        print(f"   🔍 User queries about 'programming languages'")
        print(f"   ✨ Memory is accessed - temperature boosts!")
        
        # Boost temperature
        boost = 0.4
        temperature = min(1.0, temperature + boost)
        print(f"   After access: {print_temperature_bar(temperature)}")
        
        # More time passes
        print(f"\n   Time passes again...")
        time.sleep(1)
        temperature = ambient_temp + (temperature - ambient_temp) * math.exp(-decay_rate * 10)
        print(f"   After 10s: {print_temperature_bar(temperature)}")
        
        # Another access
        print(f"\n   🔍 User asks about 'Python programming'")
        print(f"   ✨ Memory accessed again - another boost!")
        temperature = min(1.0, temperature + boost)
        print(f"   After access: {print_temperature_bar(temperature)}")
        
        print(f"\n   💡 The memory stays warm through regular use!")
    
    # Phase 3: Long-term neglect
    print(f"\n⏰ Phase 3: Long-term neglect")
    print(f"   Memory is not accessed for a long time...")
    
    for i in range(3):
        time.sleep(0.5)
        temperature = ambient_temp + (temperature - ambient_temp) * math.exp(-decay_rate * 15)
        print(f"   After 15s: {print_temperature_bar(temperature)}")
        
        if temperature < threshold:
            print(f"\n   💀 Memory temperature dropped below {threshold}")
            print(f"   🗑️  Memory is forgotten (cleaned up)")
            break
    
    # Summary
    print("\n" + "=" * 70)
    print("Summary: 'Use it or Lose it' Strategy")
    print("=" * 70)
    print("✅ Fresh memories start hot (temperature = 1.0)")
    print("✅ Unused memories cool down exponentially (Newton's Law)")
    print("✅ Accessing memories boosts their temperature (reinforcement)")
    print("✅ Regular use keeps memories alive and hot")
    print("✅ Neglected memories eventually cool and are forgotten")
    print("\n🧠 This mimics biological memory and the Ebbinghaus forgetting curve!")
    print("=" * 70)


def demonstrate_ebbinghaus_curve():
    """Demonstrate Ebbinghaus forgetting curve"""
    print("\n\n" + "=" * 70)
    print("Ebbinghaus Forgetting Curve Simulation")
    print("=" * 70)
    
    print("\n📊 Memory retention over time without reinforcement:")
    print()
    
    initial_temp = 1.0
    decay_rate = 0.1
    
    time_points = [0, 1, 5, 10, 20, 30, 50, 100]
    
    print("Time | Temperature | Retention | Visual")
    print("-" * 70)
    
    for t in time_points:
        temp = initial_temp * math.exp(-decay_rate * t)
        retention = temp * 100
        bar = "█" * int(temp * 30)
        
        print(f"{t:4d} | {temp:11.4f} | {retention:8.1f}% | {bar}")
    
    print("\n💡 This exponential decay is exactly what Ebbinghaus observed!")
    print("   Memories fade rapidly at first, then more slowly over time.")


if __name__ == "__main__":
    print("\n🧠" * 35)
    print("\nBionicMemory: Interactive Memory Decay Demonstration")
    print("\n🧠" * 35)
    
    simulate_memory_lifecycle()
    demonstrate_ebbinghaus_curve()
    
    print("\n\n✨ Demonstration complete!")
    print("\nTo see this in action with the full system, run:")
    print("  1. python main.py")
    print("  2. python examples/test_api.py")
    print()
