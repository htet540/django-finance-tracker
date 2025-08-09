def model_changes(instance, old_instance, fields):
    """Return dict of changed {field: (old, new)} for given fields."""
    changes = {}
    for f in fields:
        old = getattr(old_instance, f, None)
        new = getattr(instance, f, None)
        if old != new:
            changes[f] = (old, new)
    return changes