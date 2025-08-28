# Obsidian-extension
A script to access obsidian notes from a central server by clients on a network
X-Obsadian is built on fast api and uvicorn to host

As part of scripting and adding custom features to my stripped windows 10, Working from a VM, I need to get information from my Obsidian notes on my ost machine.
Moving to and fro in tabs and programs was tideous so I decided to crete a solution resulting to this. 

As a result, some of the details (such as IP address, Port numbers, directories) are static which can be modified as suited)
#I've left comments on the parts you must alter.

Offers features 
1. query from obsidian directly
2. export files from client to obsidian
3. Write directly into obsidian

NB: after export or write, use <X-obsidian.py reload > to refresh the database
