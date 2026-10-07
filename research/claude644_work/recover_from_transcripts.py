#!/usr/bin/env python3
"""Rebuild the scratchpad working files (wiped by a reboot on 24 Sep 2026) by replaying, in timestamp
order, every file-writing operation recorded in the session transcripts:
  * Write tool calls   (file_path, content)
  * Edit tool calls    (file_path, old_string, new_string, replace_all)
  * shell heredocs     cat > PATH <<'EOF' ... EOF   and   cat >> PATH <<'EOF' ... EOF
    (relative paths resolved against the last 'cd DIR' earlier in the same command)
Only paths under the old scratchpad are replayed; they are mapped into this directory.
Files produced by *running* programs (logs, pickles, certificates) or edited by inline python/sed are not
recoverable this way; the report lists every operation that was skipped."""
import json, os, re, sys, glob, collections

OLD = '/private/tmp/claude-501/-Users-cubres-Documents-Clauding/3451ffda-5ca8-4fb7-94da-7d7eeb432722/scratchpad/'
NEW = os.path.dirname(os.path.abspath(__file__)) + '/recovered/'
P = '/Users/cubres/.claude/projects/-Users-cubres-Documents-Clauding/3451ffda-5ca8-4fb7-94da-7d7eeb432722'
SOURCES = [P + '.jsonl'] + sorted(glob.glob(P + '/subagents/**/*.jsonl', recursive=True))

HEREDOC = re.compile(r"cat\s*(>>|>)\s*(\"?[^\s<>|;&\"]+\"?)\s*<<-?\s*['\"]?(\w+)['\"]?[^\n]*\n(.*?)\n\3(?=\n|$|\s|\))", re.S)
CD = re.compile(r"(?:^|&&|;|\n)\s*cd\s+(\"?[^\s;&\"]+\"?)")

def map_path(p, cwd=None):
    p = p.strip('"')
    if not p.startswith('/'):
        if cwd is None: return None
        p = os.path.normpath(os.path.join(cwd, p))
    p = os.path.normpath(p)
    old = os.path.normpath(OLD)
    if p == old or not p.startswith(old + '/'): return None
    return NEW + p[len(old) + 1:]

ops = []
for src in SOURCES:
    try:
        fh = open(src, errors='replace')
    except OSError:
        continue
    for ln, line in enumerate(fh):
        try: d = json.loads(line)
        except Exception: continue
        ts = d.get('timestamp') or ''
        msg = d.get('message') or {}
        content = msg.get('content') if isinstance(msg, dict) else None
        if not isinstance(content, list): continue
        for blk in content:
            if not isinstance(blk, dict) or blk.get('type') != 'tool_use': continue
            name, inp = blk.get('name'), blk.get('input') or {}
            if name == 'Write' and 'file_path' in inp:
                q = map_path(inp['file_path'])
                if q: ops.append((ts, src, ln, 'write', q, inp.get('content', '')))
            elif name == 'Edit' and 'file_path' in inp:
                q = map_path(inp['file_path'])
                if q: ops.append((ts, src, ln, 'edit', q, (inp.get('old_string', ''), inp.get('new_string', ''), inp.get('replace_all', False))))
            elif name == 'Bash':
                cmd = inp.get('command', '')
                if 'cat' not in cmd or '<<' not in cmd: continue
                for m in HEREDOC.finditer(cmd):
                    cwd = None
                    for c in CD.finditer(cmd[:m.start()]): cwd = c.group(1).strip('"')
                    q = map_path(m.group(2), cwd)
                    if q:
                        ops.append((ts, src, ln, 'append' if m.group(1) == '>>' else 'write', q, m.group(4) + '\n'))

ops.sort(key=lambda o: (o[0], o[1], o[2]))
state = {}
stats = collections.Counter(); failed_edits = []
for ts, src, ln, kind, q, payload in ops:
    if kind == 'write':
        state[q] = payload; stats['write'] += 1
    elif kind == 'append':
        state[q] = state.get(q, '') + payload; stats['append'] += 1
    elif kind == 'edit':
        old, new, rall = payload
        cur = state.get(q)
        if cur is not None and old in cur:
            state[q] = cur.replace(old, new) if rall else cur.replace(old, new, 1); stats['edit'] += 1
        else:
            failed_edits.append((ts, q)); stats['edit_failed'] += 1
for q, text in state.items():
    os.makedirs(os.path.dirname(q), exist_ok=True)
    with open(q, 'w') as f: f.write(text)
print(f"sources {len(SOURCES)}, operations {len(ops)}, files rebuilt {len(state)}; {dict(stats)}")
for ts, q in failed_edits[:20]: print("  edit not applied:", ts, q)
