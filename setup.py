from distutils.core import setup

setup(
    name='django-smtp-starttls',
    version='1.0.1',
    description='Custom SSL params for Django email backend',
    author='Stefano Brilli',
    author_email='stefanobrilli@gmail.com',
    url='https://github.com/cybercase/django-smtp-starttls',
    license='MIT',
    py_modules=('django_smtp_starttls',),
    zip_safe=True,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)