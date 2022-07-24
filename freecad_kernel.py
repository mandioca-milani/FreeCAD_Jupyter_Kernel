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
    tfile: list[tempfile._TemporaryFileWrapper] = list()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        subprocess.run([
            '/usr/bin/nohup', '/usr/bin/bash', '-c',
            # '/usr/bin/freecad --single-instance --log-file ./FreeCAD.log &>./nohup.log &',
            '/usr/bin/freecad --single-instance &>./dev/null &',
        ])

        self.tdir = tempfile.TemporaryDirectory(prefix='FreeCADJupyterKernel')

    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False, *, cell_id=None):
        self.tfile.append(tempfile.NamedTemporaryFile('wt', suffix='.py', dir=self.tdir.name))

        tfile = self.tfile[-1]
        tfile.write(code)
        tfile.seek(0)

        subprocess.run([
            '/usr/bin/nohup', '/usr/bin/bash', '-c',
            '/usr/bin/freecad --single-instance {file1} &>/dev/null &'
            .format(file1=tfile.name)
        ])

        return {
            'status': 'ok',
            'execution_count': self.execution_count,
            'payload': [],
            'user_expressions': {},
        }


if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=FreeCADKernel)
