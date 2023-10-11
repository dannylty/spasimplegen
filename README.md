```
python3 simple.py
python3 simple.py -h
```
| Argument | Type  | Default | Description                                                                                                                                 |
|----------|-------|---------|--------------------------------------------------------------------------------------------------------------------------------------------|
| `-n`     | int   | 5       | Number of procedures.                                                                                                        |
| `-l`     | float | 0.8     | Statement length factor. Higher value gives longer statement lists. Increasing this indirectly increases nesting depth. 0.0-1.0. Default 0.8.                 |
| `-b`     | float | 1.0     | Statement branch factor. 1x is the default probability for any statement to be a if/while. Anything beyond ~1.5 is ridiculous.|
| `-e`     | float | 0.5     | Expression expansion factor, Higher value gives more branched expressions. Valid range is 0.0-1.0.                          |

generates simple source code in generate.in

current processors:
* CALLS
