#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(r'd:\AmazonQ\InforQ')

from docx_reader import read_docx_full

# Read the TES-070 file
doc_path = r"C:\Users\vsilleza\Downloads\TES-070_INT001_Asset Accounts Extract_20251030_101118_v16.docx"

print("=== TES-070 CONTENT ANALYSIS ===")
content = read_docx_full(doc_path)

print(f"Document length: {len(content)} characters")
print("\n=== FIRST 2000 CHARACTERS ===\n")
print(content[:2000])

# Look for Section 3 content
lines = content.split('\n')
print(f"\n=== DOCUMENT HAS {len(lines)} LINES ===\n")

# Show lines that contain "3" or "FR" or "CUSTOM"
for i, line in enumerate(lines[:100]):  # First 100 lines
    if any(keyword in line.upper() for keyword in ['3\t', 'FR 1.', 'CUSTOM', 'SECTION']):
        print(f"Line {i}: {line}")

in_section_3 = False
fr_sections = []
current_fr = None

for i, line in enumerate(lines):
    if '3\tCUSTOM EXTENSION UNIT TEST DETAILED RESULTS' in line or 'CUSTOM EXTENSION UNIT TEST DETAILED RESULTS' in line:
        in_section_3 = True
        print(f"Found Section 3 at line {i}: {line}")
        continue
    
    if in_section_3:
        if line.startswith('4\t') or '4\tProblems' in line:  # Section 4 starts
            break
        
        if line.startswith('FR 1.') or 'FR 1.' in line:
            current_fr = line.strip()
            fr_sections.append({
                'header': current_fr,
                'line': i,
                'content': []
            })
            print(f"Found {current_fr} at line {i}")
        elif current_fr and fr_sections:
            fr_sections[-1]['content'].append(line)

print(f"\nFound {len(fr_sections)} FR sections:")
for i, fr in enumerate(fr_sections):
    print(f"\n--- {fr['header']} ---")
    content_preview = '\n'.join(fr['content'][:10])  # First 10 lines
    print(content_preview)
    if len(fr['content']) > 10:
        print(f"... and {len(fr['content']) - 10} more lines")