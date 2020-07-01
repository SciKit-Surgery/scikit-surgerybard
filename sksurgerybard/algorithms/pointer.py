"""Classes for processing BARD pointer events"""

from os import mkdir, path
from time import time
from numpy import savetxt, reshape


class BardPointerWriter():
    """
    Class to locate the pointer tip and write to file
    """
    def __init__(self, transform_manager, out_dir, pointer_tip):
        """
        param: transform manager to containing pointer tracking matrix
        param: directory to write to
        param: pointer calibration
        :raises: Attribute Error if transform mananger doesn't implement get.
        :raises: TypeError of out_dir not str or path
        :raises: FileNotFoundError if out_dir not writeable
        """

        try:
            transform_manager.get("unused")
        except ValueError:
            pass
        except AttributeError:
            raise AttributeError("transform manager has no method get",
                                 ", check type")

        self._tm = transform_manager
        self._outdir = out_dir
        self._pointer_tip = pointer_tip

        try:
            self._matoutdir = path.join(out_dir, 'bard_pointer_matrices')
            if not path.isdir(self._matoutdir):
                mkdir(self._matoutdir)

            self._tipoutdir = path.join(out_dir, 'bard_pointer_tips')
            if not path.isdir(self._tipoutdir):
                mkdir(self._tipoutdir)
        except TypeError:
            raise TypeError("out dir does not appear to be a valid directory")
        except FileNotFoundError:
            raise FileNotFoundError("out dir is not a writeable directory")

    def write_pointer_tip(self):
        """
        Locates pointer and tip, and writes to file
        """

        pointermat = None
        try:
            pointermat = self._tm.get("pointerref2modelreference")
        except ValueError:
            print("No pointer matrix available")

        if pointermat is not None:
            filename = '{0:d}.txt'.format(int(time()*1e7))
            savetxt(path.join(self._matoutdir, filename), pointermat)
            print("Pointer matrix written to ",
                  path.join(self._matoutdir, filename))

            if self._pointer_tip is not None:
                pointer_tip_location = \
                    pointermat[0:3, 0:3] @ reshape(self._pointer_tip,
                                                   (3, 1)) + \
                    reshape(pointermat[0:3, 3], (3, 1))

                savetxt(path.join(self._tipoutdir, filename),
                        pointer_tip_location)
                print("Pointer tip written to ",
                      path.join(self._tipoutdir, filename))
