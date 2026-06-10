#!/usr/bin/env python3
import json
import sys
import os
import hashlib
from datetime import datetime

CASES_FILE = os.path.expanduser("~/.claude/skills/alert-analyzer/knowledge/cases.db.json")

def save_case(case):
    # 确保目录存在
    os.makedirs(os.path.dirname(CASES_FILE), exist_ok=True)
    
    # 加载现有案例
    try:
        with open(CASES_FILE, 'r') as f:
            cases = json.load(f)
    except:
        cases = []
    
    # 生成唯一ID（基于内容哈希，避免重复）
    case_id = hashlib.md5(f"{case.get('original','')}{case.get('script_name','')}".encode()).hexdigest()[:8]
    case['id'] = case_id
    case['created_at'] = datetime.now().isoformat()
    
    # 检查是否已存在
    for i, existing in enumerate(cases):
        if existing.get('id') == case_id:
            cases[i] = case  # 更新
            break
    else:
        cases.append(case)
    
    # 限制案例库大小（最多500条，保留最新的）
    if len(cases) > 500:
        cases = cases[-500:]
    
    with open(CASES_FILE, 'w') as f:
        json.dump(cases, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 案例已保存，当前案例库共 {len(cases)} 条")

if __name__ == "__main__":
    case = json.loads(sys.argv[1])
    save_case(case)