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
        'Frontend': {'exts': ['.html', '.css', '.js'], 'exclude_dirs': ['node_modules', 'dist', 'build', 'tests', '.venv', '.venv_lock']},
        'Backend': {'exts': ['.py'], 'exclude_dirs': ['.venv', '.venv_lock', '__pycache__', 'tests', 'alembic', 'scripts']},
        'Tests': {'exts': ['.py', '.js'], 'include_dirs': ['tests', 'test']},
        'Migrations': {'exts': ['.py', '.sql'], 'include_dirs': ['alembic', 'migrations']},
        'Infrastructure': {'exts': ['.yml', '.yaml', 'Dockerfile', '.conf'], 'exclude_dirs': []},
        'Utilities': {'exts': ['.py', '.sh'], 'include_dirs': ['scripts']},
    }
    
    file_counts = {cat: 0 for cat in categories}
    total_files = {cat: 0 for cat in categories}
    
    ignored = {'.git', 'node_modules', '.venv', '.venv_lock', '__pycache__', '.pytest_cache', 'dist', 'build'}
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if d not in ignored and not d.startswith('.')]
        
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            ext = os.path.splitext(filename)[1].lower()
            
            loc = count_loc_in_file(filepath)
            
            # Simple heuristic categorization
            assigned = False
            for cat, config in categories.items():
                if 'include_dirs' in config:
                    if any(inc in dirpath for inc in config['include_dirs']):
                        if ext in config['exts'] or filename in config['exts']:
                            file_counts[cat] += loc
                            total_files[cat] += 1
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
                            total_files[cat] += 1
                            break
                            
    return file_counts, total_files

def main():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    counts, files = get_files_by_category(root_dir)
    
    prod_loc = counts.get('Frontend', 0) + counts.get('Backend', 0)
    prod_files = files.get('Frontend', 0) + files.get('Backend', 0)
    total = sum(counts.values())
    target = 55000
    
    print("========================================")
    print("CITYBUS CODEBASE PRODUCTION LOC STATUS")
    print("========================================")
    print()
    print(f"Frontend LOC:   {counts.get('Frontend', 0):>8}  ({files.get('Frontend', 0)} files)")
    print(f"Backend LOC:    {counts.get('Backend', 0):>8}  ({files.get('Backend', 0)} files)")
    print(f"Production LOC: {prod_loc:>8}  ({prod_files} files)")
    print("----------------------------------------")
    print(f"Tests:          {counts.get('Tests', 0):>8}  ({files.get('Tests', 0)} files)")
    print(f"Migrations:     {counts.get('Migrations', 0):>8}  ({files.get('Migrations', 0)} files)")
    print(f"Infrastructure: {counts.get('Infrastructure', 0):>8}  ({files.get('Infrastructure', 0)} files)")
    print(f"Utilities:      {counts.get('Utilities', 0):>8}  ({files.get('Utilities', 0)} files)")
    print()
    print(f"TOTAL CODE LOC: {total:>8}")
    print(f"TARGET PROD LOC:{target:>8}")
    print()
    print(f"REMAINING PROD: {max(0, target - prod_loc):>8}")
    status = "COMPLETE" if prod_loc >= 50000 else "EXPANSION NEEDED"
    print(f"STATUS:         {status}")
    print("========================================")

if __name__ == '__main__':
    main()
