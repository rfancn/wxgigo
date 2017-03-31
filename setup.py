from setuptools import setup

setup(
    name='wxgigo',
    version='0.1',
    description='The framework to rapidly develop app with Wechat Media Platform or Wechat API',
    url='http://wxgigo.guanxigo.com',
    author='Ryan Fan',
    author_email='reg_info@126.com',
    license='MIT',
    packages=['wxgigo'],
    # required packages while install wxgigo package
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'wxgigo-admin = wxgigo.management:execute_from_command_line',
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    zip_safe=False
)