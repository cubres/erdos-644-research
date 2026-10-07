# Minimal converter paper_0865.tex -> paper_0865.md (handles only the constructs used in that file).
import re, sys
src = open(sys.argv[1]).read()
out_path = sys.argv[2]

def expand_macro(s, name, left, right):
    # replace \name{arg} by left arg right, with brace matching
    key = '\\' + name + '{'
    while True:
        i = s.find(key)
        if i < 0: return s
        j = i + len(key); depth = 1; k = j
        while depth:
            if s[k] == '{': depth += 1
            elif s[k] == '}': depth -= 1
            k += 1
        s = s[:i] + left + s[j:k-1] + right + s[k:]

s = src
title = re.search(r'\\title\[[^\]]*\]\{(.*?)\}\n', s).group(1)
date = re.search(r'\\date\{(.*?)\}\n', s).group(1)
s = s[s.index('\\begin{document}') + len('\\begin{document}'):]
s = s.replace('\\end{document}', '')

# --- numbering of sections and theorem-like environments, collect labels ---
envs = ['theorem', 'lemma', 'proposition', 'corollary', 'definition', 'remark']
labels = {}
sec = 0; cnt = 0; appendix = False
tokens = re.finditer(r'\\appendix|\\section\{|\\begin\{(' + '|'.join(envs) + r')\}(\[[^\]]*\])?(\\label\{([^}]*)\})?', s)
secnames = []
for m in tokens:
    t = m.group(0)
    if t == '\\appendix':
        appendix = True; sec = 0; continue
    if t.startswith('\\section'):
        sec += 1; cnt = 0
        # label right after section title
        rest = s[m.end():]
        depth = 1; k = 0
        while depth:
            if rest[k] == '{': depth += 1
            elif rest[k] == '}': depth -= 1
            k += 1
        lab = re.match(r'\\label\{([^}]*)\}', rest[k:])
        num = chr(ord('A') + sec - 1) if appendix else str(sec)
        if lab: labels[lab.group(1)] = num
        continue
    cnt += 1
    num = (chr(ord('A') + sec - 1) if appendix else str(sec)) + '.' + str(cnt)
    if m.group(4): labels[m.group(4)] = num

# --- structural replacements ---
def sub_sections(s):
    out = []; sec = 0; appendix = False; pos = 0
    for m in re.finditer(r'\\appendix|\\section\{|\\subsection\*\{', s):
        out.append(s[pos:m.start()])
        t = m.group(0)
        if t == '\\appendix':
            appendix = True; sec = 0; pos = m.end(); continue
        rest = s[m.end():]; depth = 1; k = 0
        while depth:
            if rest[k] == '{': depth += 1
            elif rest[k] == '}': depth -= 1
            k += 1
        name = rest[:k-1]
        if t.startswith('\\section'):
            sec += 1
            num = ('Appendix ' + chr(ord('A') + sec - 1)) if appendix else str(sec)
            out.append('\n## ' + num + '. ' + name + '\n')
        else:
            out.append('\n### ' + name + '\n')
        pos = m.end() + k
        lab = re.match(r'\\label\{[^}]*\}', s[pos:])
        if lab: pos += lab.end()
    out.append(s[pos:])
    return ''.join(out)
s = sub_sections(s)

cnt_iter = {'n': 0}
def env_open(m):
    env = m.group(1); opt = m.group(2);
    name = env.capitalize()
    return '\n**' + name + ' ' + '{{NUM}}' + (' (' + opt[1:-1] + ')' if opt else '') + '.** '
# assign numbers in order of appearance
order = []
for m in re.finditer(r'\\begin\{(' + '|'.join(envs) + r')\}(\[[^\]]*\])?(\\label\{([^}]*)\})?', s):
    order.append(m)
nums_in_order = []
sec = 0; cnt = 0; appendix = False
for m in re.finditer(r'\n## (Appendix )?([0-9A-Z]+)\.|\\begin\{(' + '|'.join(envs) + r')\}', s):
    if m.group(0).startswith('\n## '):
        sec_label = m.group(2); cnt = 0; continue
    cnt += 1; nums_in_order.append(sec_label + '.' + str(cnt))
it = iter(nums_in_order)
def env_open2(m):
    env = m.group(1); opt = m.group(2)
    return '\n**' + env.capitalize() + ' ' + next(it) + (' (' + opt[1:-1] + ')' if opt else '') + '.** '
s = re.sub(r'\\begin\{(' + '|'.join(envs) + r')\}(\[[^\]]*\])?(\\label\{[^}]*\})?\n?', env_open2, s)
s = re.sub(r'\\end\{(' + '|'.join(envs) + r')\}', '\n', s)
s = s.replace('\\begin{proof}\n', '\n*Proof.* ').replace('\\begin{proof}', '\n*Proof.* ')
s = s.replace('\\end{proof}', ' ∎\n')
s = s.replace('\\begin{abstract}\n', '## Abstract\n\n').replace('\\end{abstract}', '')
s = s.replace('\\maketitle', '')

# lists
def conv_lists(s):
    lines = s.split('\n'); out = []; stack = []
    for ln in lines:
        st = ln.strip()
        if st.startswith('\\begin{itemize}'): stack.append(['-', 0]); continue
        if st.startswith('\\begin{enumerate}'): stack.append(['1', 0]); continue
        if st.startswith('\\end{itemize}') or st.startswith('\\end{enumerate}'):
            stack.pop(); out.append(''); continue
        mset = re.match(r'\\setcounter\{enumi\}\{(\d+)\}', st)
        if mset: stack[-1][1] = int(mset.group(1)); continue
        if st.startswith('\\item') and stack:
            body = st[len('\\item'):].strip()
            if stack[-1][0] == '-': out.append('- ' + body)
            else:
                stack[-1][1] += 1; out.append(str(stack[-1][1]) + '. ' + body)
            continue
        out.append(ln)
    return '\n'.join(out)
s = conv_lists(s)

# bibliography
s = s.replace('\\begin{thebibliography}{9}', '\n## References\n').replace('\\end{thebibliography}', '')
s = re.sub(r'\\bibitem\{([^}]*)\}', r'- [\1]', s)

# refs, cites
s = re.sub(r'\\cite\[([^\]]*)\]\{([^}]*)\}', r'[\2, \1]', s)
s = re.sub(r'\\cite\{([^}]*)\}', r'[\1]', s)
s = re.sub(r'\\ref\{([^}]*)\}', lambda m: labels.get(m.group(1), '??'), s)
s = re.sub(r'\\label\{[^}]*\}', '', s)

# display math
s = re.sub(r'\\begin\{equation\*\}\\tag\{([^}]*)\}\s*(.*?)\\end\{equation\*\}', lambda m: '$$\n' + m.group(2).strip() + ' \\tag{' + m.group(1) + '}\n$$', s, flags=re.S)
s = re.sub(r'\\\[\s*(.*?)\s*\\\]', lambda m: '\n$$\n' + m.group(1) + '\n$$\n', s, flags=re.S)

# macros inside math
s = expand_macro(s, 'ceil', '\\lceil ', '\\rceil ')
s = expand_macro(s, 'floor', '\\lfloor ', '\\rfloor ')
s = s.replace('\\cH', '\\mathcal H')
# text formatting
s = expand_macro(s, 'emph', '*', '*')
s = expand_macro(s, 'textbf', '**', '**')
s = expand_macro(s, 'textit', '*', '*')
s = expand_macro(s, 'texttt', '`', '`')
s = s.replace('\\_', '_')
for a, b in [('\\H{o}', 'ő'), ("\\'c", 'ć'), ("\\'a", 'á'), ('\\#', '#'), ('``', '"'), ("''", '"'),
             ('\\medskip', ''), ('\\noindent', ''), ('\\qed', '∎'), ('---', '—')]:
    s = s.replace(a, b)
s = re.sub(r'(?<![\\$0-9a-zA-Z])--(?!-)', '–', s)
s = re.sub(r'~', ' ', s)
s = re.sub(r'\n{3,}', '\n\n', s)
header = '# ' + title.replace('$(7,2)$', '(7,2)') + '\n\n*[Author names to be added]* — ' + date + '\n\n' \
         '*Plain-text mirror of `paper_0865.tex` (generated by `w5_paper_tex2md.py`; the LaTeX file is authoritative).*\n'
open(out_path, 'w').write(header + s.strip() + '\n')
print('labels', len(labels), 'unresolved refs:', s.count('??'))
