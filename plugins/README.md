# Collections Plugins Directory

This directory can be used to ship various plugins inside an Ansible collection. Each plugin is placed in a folder that
is named after the type of plugin it is in. It can also include the `module_utils` and `modules` directory that
would contain module utils and modules respectively.

## Folder Structure Overview

### `lookup/` Folder
This folder contains lookup files used by playbooks. These files are essential for managing references between different components.

### `module_utils/` Folder
This folder includes the core library responsible for handling low-level connections to the `smc-python` library.

### `modules/` Folder
This folder holds all the necessary modules required to perform operations with SMC.
