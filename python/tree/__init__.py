import pkgutil
import unittest

__path__ = pkgutil.extend_path(__path__, __name__)
for importer, modname, ispkg in pkgutil.walk_packages(path=__path__, prefix=__name__+'.'):
    __import__(modname)


def run():
    suite = unittest.TestLoader().discover(".")
    #suite = unittest.TestLoader().loadTestsFromTestCase(region_test)
    unittest.TextTestRunner(verbosity=2).run(suite)
