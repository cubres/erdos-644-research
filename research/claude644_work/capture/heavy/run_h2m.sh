#!/bin/bash
cd "$(dirname "$0")"
nohup python3 h2_margin_climb.py 1 60000 1 4 > h2m_1.log 2>&1 &
nohup python3 h2_margin_climb.py 2 60000 1 5 > h2m_2.log 2>&1 &
nohup python3 h2_margin_climb.py 3 60000 1 4 > h2m_3.log 2>&1 &
nohup python3 h2_margin_climb.py 4 60000 2 6 > h2m_4.log 2>&1 &
