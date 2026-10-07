import sys
exec(open('totals.py').read().split('base = H')[0])
src = open('three_type_cert.py').read()
exec(src.split('STATS = ')[0].split('DISJ = []')[1].join(['DISJ = []\n', '']) if False else '')
