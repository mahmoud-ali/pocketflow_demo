import os

def load_data(data_dir):
    """Load data from files.
    
    Args:
        data_dir (str): Directory containing the essay text files
        
    Returns:
        data_dict: Dictionary mapping file_id to essay text
    """
    data = {}
    
    for filename in os.listdir(data_dir):
        if filename.endswith('.txt'):
            with open(os.path.join(data_dir, filename), 'r', encoding='utf-8') as f:
                data[filename] = f.read()
    
    return data

if __name__ == "__main__":
    # Example usage
    import sys
    
    # Get current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one level to project root
    project_root = os.path.dirname(current_dir)
    
    data_dir = os.path.join(project_root, "data")
    
    if os.path.exists(data_dir):
        data = load_data(data_dir)
        
        print(f"Loaded {len(data)} files")
        
        # Print a sample essay
        if data:
            sample_id = next(iter(data))
            print(f"\nSample essay (ID: {sample_id}):")
            print(f"{data[sample_id][:200]}...")
    else:
        print(f"Data directory not found.")
        print(f"Expected data directory: {data_dir}")
