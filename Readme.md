# **Property QL** 


Project is design to provide an ability to modify configuration files based on xml or  property formats.

Supported actions are INSERT, UPDATE, DELETE

Queries execution sequence is:

1. DELETE
2. UPDATE
3. INSERT

Query file (***.ql**) may contain placeholder like **${ENV_VAR}** which will be replaced (if it exists) with real environment variable before execution

# **UI** 

Run:

python3 **PropertyQLDeveloper.py**



# **CMD**

Input parameters:

_1. Source file (***.xml** or ***.properties** based file)_

_2. Query file (***.ql**)_

Ex:

python3 **_apply_config.py_** **_source_file.xml query.ql_**;

# **Output:** 

Original Source file will be saved with ***_.default_** extension (Ex.: **source_file.xml.default**)

Result will be saved to original file  (**source_file.xml**)

# **Test:** 

Unit tests and examples are available under:

* **test/case/service/propertyQL**

* **test/case/service/xmlQL**



