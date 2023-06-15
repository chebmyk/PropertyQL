# **Property QL** 


Project is design to provide an ability to modify configuration files based on xml or  property format

Query file may contain placeholder like **${ENV_VAR}** which will be replaced with real environment variable before execution

# **UI** 

Run:

python3 **PropertyQLDeveloper.py**



# **CMD**

Input parameters:

_1. Source file (***.xml** or ***.properties** based file)_

_2. Query file (***.ql**)_

python3 apply_config.py source_file.xml query.ql;

# **Output:** 

Original Source file will be saved with ***_.default_** extension (source_file.xml.default)

Result will be saved to original file  (source_file.xml)

# **Test:** 

Unit tests and examples are available under:

* **test/case/service/propertyQL**

* **test/case/service/xmlQL**



