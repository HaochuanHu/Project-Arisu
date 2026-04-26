import base64, os, sys

# Run from the script's own folder — no matter who the Windows user is.
HERE = os.path.dirname(os.path.abspath(__file__))

TPL = os.path.join(HERE, 'chess_tpl2_fixed.html')
# Arisu portraits
S2 = os.path.join(HERE, 'S2.png')               # Arisu calm
S1 = os.path.join(HERE, 'S1.png')               # Arisu annoyed (PNG binary)
# Horikita portraits
H1    = os.path.join(HERE, 'H1.PNG')            # Horikita calm
H2    = os.path.join(HERE, 'H2.PNG')            # Horikita frustrated
# Ayanokouji portraits
A1    = os.path.join(HERE, 'A1.PNG')            # Ayanokouji calm
A2    = os.path.join(HERE, 'A2.PNG')            # Ayanokouji intense
# Engine & output
SF_JS = os.path.join(HERE, 'stockfish.js')
OUT   = os.path.join(HERE, 'chess_final.html')

REQUIRED = {
    'template':          TPL,
    'S2.png (Arisu calm)':      S2,
    'S1.png (Arisu annoyed)':   S1,
    'H1.PNG (Horikita calm)':   H1,
    'H2.PNG (Horikita frust.)': H2,
    'A1.PNG (Ayanokouji calm)': A1,
    'A2.PNG (Ayanokouji int.)': A2,
}

print('\n=== Chess Final Builder ===\n')

print('Checking files...')
for label, path in REQUIRED.items():
    ok = os.path.exists(path)
    print(f'  {"OK" if ok else "MISSING"} {label}: {path}')
sf_present = os.path.exists(SF_JS)
print(f'  {"OK" if sf_present else "SKIP"} stockfish.js: {SF_JS} ' +
      ('(will bundle for offline play)' if sf_present else '(not found — CDN fallback will be used)'))

missing = [p for p in REQUIRED.values() if not os.path.exists(p)]
if missing:
    print('\nOne or more required files are missing. Aborting.')
    input('\nPress Enter to close...')
    sys.exit(1)

print('\nReading template...')
with open(TPL, 'r', encoding='utf-8') as f:
    html = f.read()
print(f'  Template: {len(html):,} chars')

REQUIRED_PLACEHOLDERS = [
    '%%CALM_B64%%', '%%ANNOYED_B64%%',
    '%%HORIKITA_CALM%%', '%%HORIKITA_FRUSTRATED%%',
    '%%AYANO_CALM%%', '%%AYANO_INTENSE%%',
]
missing_tags = [t for t in REQUIRED_PLACEHOLDERS if t not in html]
if missing_tags:
    print(f'ERROR: placeholders not found in template: {missing_tags}')
    input('\nPress Enter to close...')
    sys.exit(1)


def b64_binary(path):
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode('ascii')


def img_tag(b64, mime, alt):
    return (f'<img src="data:{mime};base64,{b64}" '
            f'style="width:100%;height:auto;display:block;border-radius:6px;" '
            f'alt="{alt}">')


print('Encoding portraits...')
# Arisu
calm_b64    = b64_binary(S2); print(f'  Arisu calm      (S2.png): {len(calm_b64):,} b64 chars')
annoyed_b64 = b64_binary(S1); print(f'  Arisu annoyed   (S1.png): {len(annoyed_b64):,} b64 chars')
# Horikita
h1_b64 = b64_binary(H1); print(f'  Horikita calm   (H1.PNG): {len(h1_b64):,} b64 chars')
h2_b64 = b64_binary(H2); print(f'  Horikita frust. (H2.PNG): {len(h2_b64):,} b64 chars')
# Ayanokouji
a1_b64 = b64_binary(A1); print(f'  Ayanokouji calm (A1.PNG): {len(a1_b64):,} b64 chars')
a2_b64 = b64_binary(A2); print(f'  Ayanokouji int. (A2.PNG): {len(a2_b64):,} b64 chars')

html = html.replace('%%CALM_B64%%',            img_tag(calm_b64,    'image/png', 'Arisu'))
html = html.replace('%%ANNOYED_B64%%',         img_tag(annoyed_b64, 'image/png', 'Arisu annoyed'))
html = html.replace('%%HORIKITA_CALM%%',       img_tag(h1_b64,      'image/png', 'Horikita'))
html = html.replace('%%HORIKITA_FRUSTRATED%%', img_tag(h2_b64,      'image/png', 'Horikita frustrated'))
html = html.replace('%%AYANO_CALM%%',          img_tag(a1_b64,      'image/png', 'Ayanokouji'))
html = html.replace('%%AYANO_INTENSE%%',       img_tag(a2_b64,      'image/png', 'Ayanokouji intense'))

if sf_present:
    print('\nBundling stockfish.js for offline play...')
    with open(SF_JS, 'r', encoding='utf-8') as f:
        sf_code = f.read()
    # Strip HTTP response headers if present (file may have been downloaded with headers)
    if sf_code.startswith('HTTP') and '\n\n' in sf_code:
        sf_code = sf_code[sf_code.find('\n\n')+2:]
        print('  (Stripped HTTP headers from stockfish.js)')
    # Escape any </script occurrences so the HTML parser doesn't close the element early
    sf_code = sf_code.replace('</script', r'<\/script')
    html = html.replace('%%STOCKFISH_JS%%', sf_code)
    print(f'  Bundled: {len(sf_code):,} chars ({len(sf_code)//1024} KB)')
else:
    html = html.replace('%%STOCKFISH_JS%%', '')
    print('  stockfish.js not found — leaving placeholder empty (CDN fallback active)')

print(f'\nWriting chess_final.html...')
with open(OUT, 'w', encoding='utf-8') as f:
    f.write(html)
size_kb = os.path.getsize(OUT) / 1024
print(f'  Written: {OUT}')
print(f'  Size: {size_kb:.1f} KB')
print(f'\nDone! Open {OUT} to play.')
input('\nPress Enter to close...')
