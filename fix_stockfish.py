"""
One-time script: strips HTTP response headers from stockfish.js if present.
Run this once after downloading stockfish.js via Cowork/Claude.
Double-click or run: python fix_stockfish.py
"""
import os, sys

DESKTOP = os.path.dirname(os.path.abspath(__file__))
SF_PATH = os.path.join(DESKTOP, 'stockfish.js')

print('=== fix_stockfish.py ===\n')

if not os.path.exists(SF_PATH):
    print('ERROR: stockfish.js not found on Desktop.')
    input('\nPress Enter to close...')
    sys.exit(1)

with open(SF_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

if content.startswith('HTTP') and '\n\n' in content:
    body = content[content.find('\n\n')+2:]
    with open(SF_PATH, 'w', encoding='utf-8') as f:
        f.write(body)
    print(f'Fixed! Stripped HTTP headers. stockfish.js is now {len(body):,} chars of clean JS.')
elif content.startswith('/*!') or content.startswith('var ') or content.startswith('//'):
    print('stockfish.js already looks clean — no action needed.')
else:
    print('WARNING: stockfish.js has an unexpected format. First 100 chars:')
    print(repr(content[:100]))

input('\nPress Enter to close...')
