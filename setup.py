from setuptools import setup

setup(name='jpjs9',
      version='0.1.0',
      description='',
      long_description='',
      author='V.S.',
      author_email='contact@volodymyrsavchenko.com',
      classifiers=[
        # 'Development Status :: 5 - Production/Stable',
        # 'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Astronomy',
      ],
      keywords='astronomy astrophysics image display',
      # url='https://js9.si.edu',
      license='MIT',
      packages=['jpjs9'],
      install_requires=['requests'],
      extras_require={'all': ['numpy', 'astropy']},
      zip_safe=False)
