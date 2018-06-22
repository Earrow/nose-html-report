from setuptools import setup

setup(
    name='nose_html_report',
    packages=['nose_html_report'],
    version='0.1.0',
    description='Generate an HTML report for nose',
    author='Earrow',
    author_email='earrow.liu@gmail.com',
    url='https://github.com/Earrow/nose-html-report',
    install_requires=['jinja2', 'nose'],
    package_data={
        'nose_html_report': ['templates/report.html']
    },
    keywords=['nose', 'testing', 'reporting'],
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6'
    ],
    entry_points={
        'nose.plugins.0.10': [
            'html-report = nose_html_report.html_report:HTMLReport'
        ]
    }
)
