from distutils.core import setup

setup(name="py-multistatus",
      version="0.1",
      author="Scott Hansen",
      author_email="firecat4153@gmail.com",
      url="http://firecat53.github.com/py-multistatus",
      description=("A multi-interval statusbar information script for use "
                   "with statusbars like bar and dzen"),
      long_description=(open('README.rst').read()),
      packages=['lib', 'plugins'],
      scripts=['bin/multistatus'],
      classifiers=[
          'Programming Language :: Python :: 3',
          'Operating System :: POSIX',
          'License :: OSI Approved :: MIT License',
          'Development Status :: 3 - Alpha',
          'Environment :: System :: Monitoring',
          'Environment :: X11 Applications'],
      data_files=[('share/py-multistatus', ['README.rst',
                                            'LICENSE',
                                            'status.cfg',
                                            'bin/monsterstart.py'])]
      )
