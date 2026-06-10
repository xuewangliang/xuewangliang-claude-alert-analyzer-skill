#!/usr/bin/env python3
import json
import os
import sys
import re
from difflib import SequenceMatcher

CASES_FILE = os.path.expanduser("~/.claude/skills/alert-analyzer/knowledge/cases.db.json")

def load_cases():
    try:
        with open(CASES_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def match(alert_content):
    cases = load_cases()
    if not cases:
        return None
    
    best_match = None
    best_score = 0
    
    for case in cases:
        # 匹配维度：script_content 关键词
        content_score = similarity(alert_content, case.get('original', ''))
        # 匹配维度：文件名/端口特征
        port_match = re.search(r'port[=:](\d+)', alert_content)
        case_port = case.get('port')
        port_score = 0.3 if port_match and case_port and str(port_match.group(1)) == str(case_port) else 0
        
        total = content_score * 0.7 + port_score * 0.3
        if total > best_score and total > 0.7:
            best_score = total
            best_match = case
    
    if best_match:
        return {
            'matched_case': best_match,
            'similarity': best_score
        }
    return None

if __name__ == "__main__":
    alert = sys.argv[1] if len(sys.argv) > 1 else ""
    result = match(alert)
    if result:
        print(json.dumps(result, ensure_ascii=False))
    else:
        print("null")