def normalize(values):
    # Ensure there are multiple unique values
    min_val = min(values)
    max_val = max(values)

    if min_val == max_val:
        return [0 for _ in values]  # or you could return [1] or handle it differently

    # Normalize each value to the range [0, 1]
    normalized_values = [(value - min_val) / (max_val - min_val) for value in values]
    
    return normalized_values

values = [-10, 0, 5, 15, 20]
normalized_values = normalize(values)

print(normalized_values)
