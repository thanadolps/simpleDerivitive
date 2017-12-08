# simpleDerivitive
An attempt to build a simple partial-ish differentiator using automatic-ish differentation

###### This project is created soley to be skill check for me, quality of project is never guarantee

### Basic Idea
This Program (when finished) will have 2 part
- [ ] Parsing - convert string into graph [*Prase.py*]
- [x] Differentation - using graph to calculate partial derivitive [*graph.py*]

#### Differentation
Find Differentation using graph

Input : 
dic -> dictionary for each Variable value
var -> Variable the program will respect to

There's each graph type (class) for each support operation (+ - * / **) and also constance and variable
it recive the data in constructor, the operartion node usually have two parameter whose type is another graph
after the graph has fully constructed the top layer will call `gradient(dic, var)` function that will 
try to calculate it's gradient, most of the operation will be dependent on it's parameter graph and recursivly dive down the graph node
until it reach constance or variable

