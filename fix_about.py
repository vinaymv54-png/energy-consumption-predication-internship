#!/usr/bin/env python3
"""Script to fix about.py escape sequences."""

# Read file in binary mode
with open('pages/about.py', 'rb') as f:
    content = f.read()

# Replace escaped triple quotes with regular ones
content = content.replace(b'\\"\\"\\"', b'"""')

# Write back
with open('pages/about.py', 'wb') as f:
    f.write(content)

print("about.py fixed")
