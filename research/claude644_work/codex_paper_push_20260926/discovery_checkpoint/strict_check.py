"""Standard-library checker with the documented per-type strictness extension."""
import sys,runpy
SRC='/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/b3c'
sys.path.insert(0,SRC)
import strict_types
strict_types.install()
runpy.run_path(SRC+'/check5.py',run_name='__main__')
