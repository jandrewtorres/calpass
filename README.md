# Cal Poly Virtual Assistant (CalPAss)

An intelligent assistant that knows all about the Cal Poly Statistics and 
Computer Science departments. It is a chatbot that can answer questions entered 
in by text (which can be easily extended to voice). These are questions about 
classes, offerings, instructors, basically anything that can be answered from 
this website: https://schedules.calpoly.edu

## Team Members

CSC 466 Knowledge Discovery from Data 
Prof. Foaad Khosmood
Spring 2021

- John Torres

- Alex Goodell

- Eric Parella
    
- Hunter Borlik

## How to Run CalPass

1) Run rebuild_db.py (only need to do so once)
2) Run calpass.py

## Dev notes

To export env:

`$ conda env export --name calpass > calpass_env.yml`

To create env from YAML file:

`conda env create --file calpass_env.yml`
