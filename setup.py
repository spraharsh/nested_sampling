import os
import numpy as np
from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

## Numpy header files 
numpy_lib = os.path.split(np.__file__)[0] 
numpy_include = os.path.join(numpy_lib, 'core/include') 

extensions = [Extension("nested_sampling.utils.cv_trapezoidal", ["nested_sampling/utils/cv_trapezoidal.pyx", "source/cv.c"],
                          include_dirs=[numpy_include],
                          extra_compile_args = ['-Wextra','-pedantic','-funroll-loops','-O3'],
                          ),
                ]

setup(
    name="nested_sampling",
    version='0.1', 
    description="Python implementation of the nested sampling algorithm",
    url="https://github.com/js850/nested_sampling",
    #cmdclass = {'build_ext': build_ext},
    packages=["nested_sampling",
              "nested_sampling.models",
              "nested_sampling.utils",
              "nested_sampling.tests",
             ],
    ext_modules=cythonize(extensions)
    )
