"""Secret scanner for repository files."""

import os
import re

patterns = [
    re.compile(r'HYDRA_DB_API_KEY\s*=\s*[\'"][^\'"]+[\'"]'),
    re.compile(r'sk_live_[a-zA-Z0-9_]{10,}'),
    re.compile(r'sk_test_[a-zA-Z0-9_]{10,}'),
    re.compile(r'SECRET_KEY\s*=\s*[\'"][^\'"]+[\'"]'),
]

found_secrets = []

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

for root, dirs, files in os.walk(repo_root):
    if any(ignore in root for ignore in ['.git', '.venv', 'node_modules', 'dist', 'build']):
        continue
    for f in files:
        if f in ['.env', '.env.local', 'secret_scan.py']:
            continue
        filepath = os.path.join(root, f)
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as fh:
                content = fh.read()
                for p in patterns:
                    if p.search(content):
                        found_secrets.append(filepath)
                        break
        except Exception:
            pass

if found_secrets:
    print("SECRET SCAN FAILED! Secrets found in:")
    for p in found_secrets:
        print(" -", p)
else:
    print("SECRET SCAN PASSED! No credentials or live secret keys found in stageable files.")
