# cython: language_level=3

from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
from Cython.Distutils import build_ext
import numpy as np

# setup(
# 	name='reconciliation',
# 	ext_modules = cythonize([
# 							'reconciliationICBC.py',
# 							'reconciliationABC.py',
# 							'reconciliationBOC.py',
# 							'reconciliationCCB.py',
# 							'consolechars.py',
# 							'main.py',
# 							])
# 	)
# 	

ext_modules = [

		Extension("AutoRecon", ["main.py"],
		include_dirs = [np.get_include()])
]

setup (
	name="auto reconciliation",
	cmdclass = {'build_ext':build_ext},
	ext_modules = ext_modules
	)

