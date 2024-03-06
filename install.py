#!/usr/bin/python
# Base installer helper

import sys
import os.path
import shutil

    
def main():
    try:
        import ansible
    except ImportError:
        print('Ansible module is required for installation.')
        sys.exit(1)

    # Find the module paths
    ansible_path = os.path.dirname(os.path.abspath(os.path.realpath(ansible.__file__)))
    print('ansible path: %s' % ansible_path)
    '''
    # Check to see if appropriate directories exist
    module_utils_path = os.path.join(ansible_path, 'module_utils')
    if not os.path.exists(module_utils_path):
        print('Module utils directory (%s) does not exist' % module_utils_path)
        sys.exit(1)
    if not os.path.isdir(module_utils_path):
        print('Module utils path (%s) is not a directory' % module_utils_path)
        sys.exit(1)
    '''
    # Where is this package located
    here = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))
    
    # Copy the module document fragments to the module docs directory so the 
    # documentation fragments display properly for the modules
    module_doc_path = os.path.join(ansible_path, 'plugins', 'doc_fragments')
    if not os.path.exists(module_doc_path):
        module_doc_path = os.path.join(ansible_path, 'utils', 'module_docs_fragments')
        if not os.path.exists(module_doc_path):
            print('Could not find ansible document module path: %s' % module_doc_path)
            sys.exit(1)

    here_doc_fragments = os.path.join(here, 'doc_fragments')
    for filename in os.listdir(here_doc_fragments):
        print("Copying doc fragment: %s to: %s" % (filename, module_doc_path))
        shutil.copy(os.path.join(here_doc_fragments, filename),
                    os.path.join(module_doc_path, filename))

    # Copy the base smc_util into module_utils directory
    module_util_path = os.path.join(ansible_path, 'module_utils')
    if not os.path.exists(module_util_path):
        print('Could not find ansible module_utils path!')
        sys.exit(1)
    # Check for existing .pyc
    if os.path.exists(os.path.join(module_util_path, 'smc_util.pyc')):
        os.remove(os.path.join(module_util_path, 'smc_util.pyc'))
    
    here_module_utils = os.path.join(here, 'module_utils')
    shutil.copy(os.path.join(here_module_utils, 'smc_util.py'),
                os.path.join(module_util_path, 'smc_util.py'))
    print("Copying smc_util.py to: %s" % module_util_path)

    # Copy the base smc_lookup into plugins/lookup directory
    lookup_path = os.path.join(ansible_path, 'plugins/lookup')
    if not os.path.exists(lookup_path):
        print('Could not find ansible plugins/lookup path!')
        sys.exit(1)
    # Check for existing .pyc
    if os.path.exists(os.path.join(lookup_path, 'smc_lookup.pyc')):
        os.remove(os.path.join(lookup_path, 'smc_lookup.pyc'))

    here_lookup = os.path.join(here, 'plugins/lookup')
    shutil.copy(os.path.join(here_lookup, 'smc-reference.py'),
                os.path.join(lookup_path, 'smc-reference.py'))
    shutil.copy(os.path.join(here_lookup, 'smc-element.py'),
                os.path.join(lookup_path, 'smc-element.py'))
    print("Copying smc-reference.py/smc-element.py to: %s" % lookup_path)


if __name__ == '__main__':
    main()
