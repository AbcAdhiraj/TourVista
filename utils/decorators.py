import functools

def log_action(action_name):
    """Decorator to log method calls for specific actions."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"[LOG] Performing action: {action_name}...")
            result = func(*args, **kwargs)
            print(f"[LOG] Action '{action_name}' completed successfully.")
            return result
        return wrapper
    return decorator
