import json

def analyze_commit_features(commit_data):
    """
    Simulates extracting complexity and risk features from a code commit.
    In a production environment, this would parse abstract syntax trees (AST) 
    and query historical bug databases.
    """
    modified_files = commit_data.get("modified", [])
    
    # Calculate basic churn metrics
    files_changed_count = len(modified_files)
    total_lines_added = sum([file.get("additions", 0) for file in modified_files])
    
    # Simulate a complexity weight based on file types touched
    # Legacy files or complex backend logic carry higher inherent risk
    complexity_weight = 1.0
    for file in modified_files:
        filename = file.get("filename", "")
        if filename.endswith(".legacy.py") or filename.endswith(".c"):
            complexity_weight += 0.5
            
    # Compile the final feature set to send to the ML model
    features = {
        "commit_id": commit_data.get("id", "unknown"),
        "files_changed": files_changed_count,
        "lines_added": total_lines_added,
        "calculated_complexity": files_changed_count * complexity_weight
    }
    
    return features

# Example usage for testing purposes
if __name__ == "__main__":
    sample_payload = {
        "id": "a1b2c3d4",
        "modified": [
            {"filename": "auth_service.legacy.py", "additions": 45},
            {"filename": "utils.py", "additions": 5}
        ]
    }
    extracted = analyze_commit_features(sample_payload)
    print(f"Extracted Features: {json.dumps(extracted, indent=2)}")