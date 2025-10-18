"""Utility functions for BionicMemory"""


def format_temperature(temperature: float) -> str:
    """Format temperature with emoji indicator"""
    if temperature > 0.7:
        return f"🔥 {temperature:.2f}"
    elif temperature > 0.3:
        return f"🌡️ {temperature:.2f}"
    else:
        return f"❄️ {temperature:.2f}"


def format_time_elapsed(seconds: float) -> str:
    """Format elapsed time in human-readable format"""
    if seconds < 60:
        return f"{seconds:.0f}s"
    elif seconds < 3600:
        return f"{seconds/60:.0f}m"
    elif seconds < 86400:
        return f"{seconds/3600:.1f}h"
    else:
        return f"{seconds/86400:.1f}d"
