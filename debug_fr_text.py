#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from docx import Document

# Check exact FR text format
template_path = r"d:\AmazonQ\InforQ\RICE_Tester\TES-070-Template\TES-070_Custom_Extension_Unit_Test_Results_v2.0.docx"
doc = Document(template_path)

print("=== FR SECTION TEXT ANALYSIS ===")
for i, para in enumerate(doc.paragraphs):
    if 'FR 1.' in para.text:
        print(f"Line {i}: '{para.text}'")
        print(f"  Starts with 'FR 1.2': {para.text.startswith('FR 1.2')}")
        print(f"  Starts with 'FR 1.3': {para.text.startswith('FR 1.3')}")
        print(f"  Contains 'FR 1.2': {'FR 1.2' in para.text}")
        print(f"  Contains 'FR 1.3': {'FR 1.3' in para.text}")
        print()