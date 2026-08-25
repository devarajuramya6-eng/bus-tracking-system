import os
import zipfile

def create_zip(zip_filename):
    exclude_dirs = {'node_modules', 'venv', '.venv', '__pycache__', '.pytest_cache', 'dist', '.idea', '.vscode'}
    exclude_exts = {'.zip'}
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk('.'):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in exclude_exts or file == zip_filename:
                    continue
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, '.')
                arcname = rel_path.replace(os.sep, '/').replace('\\', '/')
                zipf.write(file_path, arcname)

if __name__ == '__main__':
    create_zip('Bus-FINAL-WITH-GIT.zip')
    create_zip('repo.zip')
    print("Created Bus-FINAL-WITH-GIT.zip and repo.zip successfully with complete .git history.")

