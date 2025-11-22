#!/usr/bin/env python3
"""
Deployment Verification Script
Checks if the app is ready for Streamlit Cloud deployment
"""

import os
import sys

def check_file_exists(filename):
    """Check if a required file exists"""
    if os.path.exists(filename):
        print(f"✅ {filename} exists")
        return True
    else:
        print(f"❌ {filename} is missing")
        return False

def check_file_content(filename, required_strings):
    """Check if file contains required strings"""
    if not os.path.exists(filename):
        print(f"❌ {filename} not found")
        return False
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            all_found = True
            for req_str in required_strings:
                if req_str in content:
                    print(f"✅ {filename} contains '{req_str}'")
                else:
                    print(f"❌ {filename} missing '{req_str}'")
                    all_found = False
            return all_found
    except Exception as e:
        print(f"❌ Error reading {filename}: {e}")
        return False

def main():
    print("=" * 60)
    print("Streamlit Cloud Deployment Verification")
    print("=" * 60)
    print()
    
    all_checks_passed = True
    
    # Check required files
    print("📁 Checking required files...")
    required_files = [
        "app.py",
        "requirements.txt",
        "runtime.txt",
        ".streamlit/config.toml"
    ]
    
    for file in required_files:
        if not check_file_exists(file):
            all_checks_passed = False
    
    print()
    
    # Check requirements.txt
    print("📦 Checking requirements.txt...")
    if check_file_content("requirements.txt", ["streamlit", "transformers", "gtts"]):
        print("✅ requirements.txt looks good")
    else:
        all_checks_passed = False
    
    print()
    
    # Check runtime.txt
    print("🐍 Checking runtime.txt...")
    if check_file_content("runtime.txt", ["3.11"]):
        print("✅ runtime.txt specifies Python 3.11")
    else:
        all_checks_passed = False
    
    print()
    
    # Check config.toml
    print("⚙️ Checking .streamlit/config.toml...")
    if check_file_content(".streamlit/config.toml", ["headless = true"]):
        print("✅ Config is set for cloud deployment (headless = true)")
    else:
        print("⚠️  Warning: headless should be true for Streamlit Cloud")
        all_checks_passed = False
    
    print()
    
    # Check app.py structure
    print("📄 Checking app.py structure...")
    if os.path.exists("app.py"):
        with open("app.py", 'r', encoding='utf-8') as f:
            content = f.read()
            checks = {
                "Has main() function": "def main()" in content,
                "Has if __name__ == '__main__'": 'if __name__ == "__main__"' in content,
                "Uses st.set_page_config": "st.set_page_config" in content,
                "Has error handling": "try:" in content and "except" in content,
            }
            
            for check_name, result in checks.items():
                if result:
                    print(f"✅ {check_name}")
                else:
                    print(f"⚠️  {check_name} - may cause issues")
                    # Not critical, so don't fail
    
    print()
    print("=" * 60)
    if all_checks_passed:
        print("✅ All critical checks passed! App should deploy successfully.")
        print()
        print("Next steps:")
        print("1. Push to GitHub: git push origin main")
        print("2. Deploy on Streamlit Cloud: https://share.streamlit.io")
        print("3. Wait for deployment (2-5 minutes)")
        return 0
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

