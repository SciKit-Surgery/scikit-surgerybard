from numpy import savetxt, reshape
from os import mkdir, path 

class BardPointerWriter():
    def __init__(self, transform_manager, out_dir, pointer_tip):
        self._tm = transform_manager
        self._outdir = out_dir
        self._pointer_tip = pointer_tip

    def write_pointer_tip(self):
        pointermat = None
        try:
            pointermat = self._tm.get("pointerref2modelreference")
        except ValueError:
            print("No pointer matrix available")

        if pointermat is not None:
            matoutdir = path.join(self._outdir, 'bard_pointer_matrices')
            filename = '{0:d}.txt'.format(int(time()*1e7))
        
            if not path.isdir(matoutdir):
                mkdir(matoutdir)
         
            savetxt(path.join(matoutdir, filename), pointermat)
            print("Pointer matrix written to ",
                  path.join(matoutdir, filename))

            if self._pointer_tip is not None:
                tipoutdir = path.join(self._outdir, 'bard_pointer_tips')
                pointer_tip_location = \
                    pointermat[0:3, 0:3] @ reshape(self._pointer_tip,
                                                      (3, 1)) + \
                    reshape(pointermat[0:3, 3], (3, 1))
            
                if not path.isdir(tipoutdir):
                    mkdir(tipoutdir)

                savetxt(path.join(tipoutdir, filename),
                       pointer_tip_location)
                print("Pointer tip written to ",
                      path.join(tipoutdir, filename))


