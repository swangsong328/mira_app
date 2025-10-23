#!/usr/bin/env python
"""
Quick structure check script - validates code structure without requiring dependencies.
Run with: python check_structure.py
"""
from __future__ import annotations

import ast
import os
import sys
from pathlib import Path


def check_python_syntax(file_path: Path) -> tuple[bool, str]:
    """Check if a Python file has valid syntax."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            ast.parse(f.read())
        return True, "OK"
    except SyntaxError as e:
        return False, f"Syntax Error: {e}"
    except Exception as e:
        return False, f"Error: {e}"


def check_project_structure():
    """Check project structure and file syntax."""
    print("Checking Beauty Salon Project Structure...\n")
    
    base_dir = Path(__file__).parent
    errors = []
    checked = 0
    
    # Critical files to check
    critical_files = [
        'manage.py',
        'config/__init__.py',
        'config/settings/base.py',
        'config/settings/local.py',
        'config/settings/production.py',
        'config/urls.py',
        'config/wsgi.py',
        'config/asgi.py',
        'apps/accounts/models.py',
        'apps/booking/models.py',
        'apps/sitecontent/models.py',
        'apps/api/serializers.py',
        'apps/api/views.py',
        'apps/core/health.py',
        'apps/core/adapters/email.py',
        'apps/core/adapters/sms.py',
    ]
    
    print("Checking critical files...")
    for file_path in critical_files:
        full_path = base_dir / file_path
        if not full_path.exists():
            errors.append(f"[X] Missing file: {file_path}")
            print(f"  [X] {file_path} - MISSING")
        else:
            success, message = check_python_syntax(full_path)
            if success:
                print(f"  [OK] {file_path} - {message}")
                checked += 1
            else:
                errors.append(f"[X] {file_path}: {message}")
                print(f"  [X] {file_path} - {message}")
    
    # Check all Python files in apps
    print("\nChecking all app files...")
    apps_dir = base_dir / 'apps'
    if apps_dir.exists():
        for py_file in apps_dir.rglob('*.py'):
            if '__pycache__' not in str(py_file):
                success, message = check_python_syntax(py_file)
                if not success:
                    rel_path = py_file.relative_to(base_dir)
                    errors.append(f"[X] {rel_path}: {message}")
                    print(f"  [X] {rel_path} - {message}")
                else:
                    checked += 1
    
    # Check required directories
    print("\nChecking directory structure...")
    required_dirs = [
        'apps/accounts',
        'apps/booking',
        'apps/sitecontent',
        'apps/core',
        'apps/api',
        'templates',
        'templates/components',
        'templates/booking',
        'templates/sitecontent',
        'templates/accounts',
        'templates/emails',
        'static',
        'static/css',
    ]
    
    for dir_path in required_dirs:
        full_path = base_dir / dir_path
        if not full_path.exists():
            errors.append(f"[X] Missing directory: {dir_path}")
            print(f"  [X] {dir_path} - MISSING")
        else:
            print(f"  [OK] {dir_path} - EXISTS")
    
    # Check required files
    print("\nChecking configuration files...")
    required_files = [
        'requirements.txt',
        'Dockerfile',
        'docker-compose.yml',
        'Makefile',
        'README.md',
        'QUICKSTART.md',
    ]
    
    for file_path in required_files:
        full_path = base_dir / file_path
        if not full_path.exists():
            errors.append(f"[X] Missing file: {file_path}")
            print(f"  [X] {file_path} - MISSING")
        else:
            print(f"  [OK] {file_path} - EXISTS")
    
    # Summary
    print("\n" + "="*60)
    print(f"Checked {checked} Python files")
    
    if errors:
        print(f"\n[X] Found {len(errors)} issues:\n")
        for error in errors:
            print(f"  {error}")
        return False
    else:
        print("\n[OK] All checks passed! Project structure is valid.")
        print("\nNext steps:")
        print("  1. Install dependencies: pip install -r requirements.txt")
        print("  2. Run migrations: python manage.py migrate")
        print("  3. Seed demo data: python manage.py seed_demo")
        print("  4. Start server: python manage.py runserver")
        return True


if __name__ == '__main__':
    success = check_project_structure()
    sys.exit(0 if success else 1)

