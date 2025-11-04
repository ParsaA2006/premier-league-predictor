"""
Setup script to create necessary directories and initialize the project
"""
import os

def create_directories():
    """Create necessary directories for the project"""
    directories = [
        "models/trained",
        "database",
        "data",
        "scripts"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")
    
    # Create __init__.py files if they don't exist
    init_files = [
        "models/__init__.py",
        "database/__init__.py",
        "data/__init__.py",
        "scripts/__init__.py"
    ]
    
    for init_file in init_files:
        if not os.path.exists(init_file):
            with open(init_file, 'w') as f:
                f.write("# Package initialization\n")
            print(f"Created: {init_file}")

if __name__ == "__main__":
    print("Setting up Premier League Predictor backend...")
    create_directories()
    print("\nSetup complete!")
    print("\nNext steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Set up .env file with your API key (optional)")
    print("3. Train models: python scripts/train_models.py")
    print("4. Run server: uvicorn main:app --reload")

