import subprocess


def test_hello():
    args = ['python', 'tests/example.py', 'hello', '--name', 'world']
    result = subprocess.run(args, stdout=subprocess.PIPE)
    assert result.stdout.decode('utf-8') == 'Hello world!\n'


def test_annoying_hello():
    args = ['python', 'tests/example.py', 'annoying_hello', '--name', 'world']
    result = subprocess.run(args, stdout=subprocess.PIPE)
    assert result.stdout.decode('utf-8') == ('Hello world!\n' * 3)


expected_help = """usage: example.py annoying_hello [-h] --name NAME [--repeats REPEATS]

Say lots of hellos

optional arguments:
  -h, --help         show this help message and exit
  --name NAME        Who to say hi to. (default: None)
  --repeats REPEATS  How many times. (default: 3)
"""

def test_help():
    args = ['python', 'tests/example.py', 'annoying_hello', '-h']
    result = subprocess.run(args, stdout=subprocess.PIPE)
    assert result.stdout.decode('utf-8') == expected_help


def test_read_list():
    args = ['python', 'tests/example.py', 'read_list', '--elements',  'a', 'b', 'c']
    result = subprocess.run(args, stdout=subprocess.PIPE)
    assert result.stdout.decode('utf-8') == "['a', 'b', 'c']\n"