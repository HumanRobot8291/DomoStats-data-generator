# DomoStats-data-generator
This Program tries to create essential data of Domo Stats for testing various Data Governance Practices.

# What this code provides?
Fake data with as much realism as you may need to perform tests on Domostats data.

# Quality requirements satisafied as follows:
1) All ids are unique and reused.
2) All relationships between datasets, owners, ETLs are logically what you would expect from real data.
3) The data is of the type that it can have the nested complexity which you may need to test some complex data governance tests.
4) Data contains last accessed timestamp that is what you would expect in real datasets and can be used to find unused data assets.

# How to use?
Just run the d_gen_V2.py file and it will create the data you need for DomoStats.
