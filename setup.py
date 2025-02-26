from setuptools import setup, find_packages

setup(
    name='q-tic-tac-toe',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'qiskit',
        'numpy',
        'matplotlib',
        'IPython',
        'math',
        'copy',
        'sys',
        'cv2',
        'PIL',
        'qiskit-aer',
    ],
)
