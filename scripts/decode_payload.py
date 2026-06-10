#!/usr/bin/env python3
import json
import sys
import base64
import urllib.parse
import re

def decode_all(text):
    results = {}
    original = text.strip()
    results['original'] = original
    
    # Base64 检测与解码
    base64_pattern = re.compile(r'^[A-Za-z0-9+/]*={0,2}$')
    if base64_pattern.match(original) and len(original) % 4 == 0:
        try:
            decoded = base64.b64decode(original).decode('utf-8', errors='ignore')
            results['base64_decoded'] = decoded
        except:
            pass
    
    # URL 解码
    url_decoded = urllib.parse.unquote_plus(original)
    if url_decoded != original:
        results['url_decoded'] = url_decoded
    
    # 递归解码（如果解码后仍是编码）
    if 'base64_decoded' in results and base64_pattern.match(results['base64_decoded']):
        try:
            double_decoded = base64.b64decode(results['base64_decoded']).decode('utf-8', errors='ignore')
            results['base64_twice'] = double_decoded
        except:
            pass
    
    return results

if __name__ == "__main__":
    payload = sys.argv[1] if len(sys.argv) > 1 else ""
    result = decode_all(payload)
    print(json.dumps(result, ensure_ascii=False))