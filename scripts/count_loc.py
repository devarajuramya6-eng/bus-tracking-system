import os
import sys

def count_loc_in_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            # Meaningful lines: not empty and not just whitespace
            meaningful_lines = [line for line in lines if line.strip()]
            return len(meaningful_lines)
    except Exception:
        return 0

def get_files_by_category(root_dir):
    categories = {
        'Frontend': {'exts': ['.html', '.css', '.js'], 'exclude_dirs': ['node_modules', 'dist', 'build']},
        'Backend': {'exts': ['.py'], 'exclude_dirs': ['.venv', '__pycache__', 'tests', 'alembic', 'scripts']},
        'Tests': {'exts': ['.py', '.js'], 'include_dirs': ['tests', 'test']},
        'Migrations': {'exts': ['.py', '.sql'], 'include_dirs': ['alembic', 'migrations']},
        'Infrastructure': {'exts': ['.yml', '.yaml', 'Dockerfile', '.conf'], 'exclude_dirs': []},
        'Utilities': {'exts': ['.py', '.sh'], 'include_dirs': ['scripts']},
    }
    
    file_counts = {cat: 0 for cat in categories}
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Exclude common directories
        dirnames[:] = [d for d in dirnames if d not in ['.git', 'node_modules', '.venv', '__pycache__']]
        
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            ext = os.path.splitext(filename)[1]
            
            loc = count_loc_in_file(filepath)
            
            # Simple heuristic categorization
            assigned = False
            for cat, config in categories.items():
                if 'include_dirs' in config:
                    if any(inc in dirpath for inc in config['include_dirs']):
                        if ext in config['exts'] or filename in config['exts']:
                            file_counts[cat] += loc
                            assigned = True
                            break
            
            if not assigned:
                for cat, config in categories.items():
                    if 'exclude_dirs' in config:
                        if any(exc in dirpath for exc in config['exclude_dirs']):
                            continue
                    
                    if 'include_dirs' not in config:
                        if ext in config['exts'] or filename in config['exts']:
                            file_counts[cat] += loc
                            break
                            
    return file_counts

def main():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    counts = get_files_by_category(root_dir)
    
    total = sum(counts.values())
    target = 60000
    
    print("========================================")
    print("CITYBUS CODEBASE LOC STATUS")
    print("========================================")
    print()
    print(f"Frontend:       {counts.get('Frontend', 0)}")
    print(f"Backend:        {counts.get('Backend', 0)}")
    print(f"Tests:          {counts.get('Tests', 0)}")
    print(f"Migrations:     {counts.get('Migrations', 0)}")
    print(f"Infrastructure: {counts.get('Infrastructure', 0)}")
    print(f"Utilities:      {counts.get('Utilities', 0)}")
    print()
    print(f"TOTAL: {total}")
    print(f"TARGET: {target}")
    print()
    print(f"REMAINING: {max(0, target - total)}")
    status = "COMPLETE" if total >= target else "CONTINUE"
    print(f"STATUS: {status}")
    print("========================================")

if __name__ == '__main__':
    main()
