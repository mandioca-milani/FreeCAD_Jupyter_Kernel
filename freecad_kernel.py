import typing as t
from ipykernel.kernelbase import Kernel
import subprocess
import tempfile


class FreeCADKernel (Kernel):
    implementation: str = 'freecad_kernel'
    implementation_version: str = '0.1'
    banner: str = 'FreeCAD'
    language_info: t.Dict[str, object] = {
        'name': 'python',
        'mimetype': 'text/x-python',
        'file_extension': '.py'
    }

    tdir: tempfile.TemporaryDirectory
    tfile: tempfile._TemporaryFileWrapper

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        subprocess.run([
            '/usr/bin/nohup', '/usr/bin/bash', '-c',
            '/usr/bin/freecad --single-instance --log-file ./FreeCAD.log &>./nohup.log &'
        ])

        self.tdir = tempfile.TemporaryDirectory(prefix='FreeCADJupyterKernel')
        self.tfile = tempfile.NamedTemporaryFile('wt', suffix='.py', dir=self.tdir.name)

    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False, *, cell_id=None):
        self.tfile.truncate(0)
        self.tfile.write(code)
        self.tfile.seek(0)

        subprocess.run([
            '/usr/bin/nohup', '/usr/bin/bash', '-c',
            '/usr/bin/freecad --single-instance {file1} &>/dev/null &'
            .format(file1=self.tfile.name)
        ])

        return {
            'status': 'ok',
            'execution_count': self.execution_count,
            'payload': [],
            'user_expressions': {},
        }
