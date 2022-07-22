from .freecad_kernel import FreeCADKernel
from ipykernel.kernelapp import IPKernelApp

if __name__ == '__main__':
    IPKernelApp.launch_instance(kernel_class=FreeCADKernel)
