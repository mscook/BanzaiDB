Getting study metadata into BanzaiDB
====================================

Here we will walk you through populating the metadata table into a freshly 
initalised BanzaiDB database.


Absolute requirements
---------------------

1) The study metadata **must be in** CSV or XLS [#]_ format,
2) The first row of the CSV or XLS **contains row headers**,
3) **There should be no missing data (empty cells)**. Please use *null* to 
   represent missing cell data. Unknown may also be used. *null* should be 
   used when it's absolutely known that the information does not exist, 
   while *unknown* is used when it's actually unknown if the data may exist, 
4) The strain identifier **must be provided**. The row header for the strain 
   identifier should be **StrainID**. If this is not the case please note the 
   row header as you'll need it when populating the table,


User considerations
-------------------

1) We will guess the type (i.e string, number etc.). If some numbers are 
   really meant to be strings please note the correct type for each header 
   element as it will be needed when populating the table. See the following 
   table of relationship between Python and JSON types:


.. _py-to-json-table:

   +-------------------+---------------+
   | Python            | JSON          |
   +===================+===============+
   | dict              | object        |
   +-------------------+---------------+
   | list, tuple       | array         |
   +-------------------+---------------+
   | str, unicode      | string        |
   +-------------------+---------------+
   | int, long, float  | number        |
   +-------------------+---------------+
   | True              | true          |
   +-------------------+---------------+
   | False             | false         |
   +-------------------+---------------+
   | None              | null          |
   +-------------------+---------------+



.. [#] Metadata provided in XLS in converted to CSVKit. 
