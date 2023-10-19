```
python3 simple.py (-h)
python3 format.py
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

Samples:
generate.in:
```
procedure proc1 {
    read var1;
}
procedure proc2 {
    read var2;
    if (16 != (var2)) then {
        read var3;
        while ((18 + var1) == 100 * (((var3 + 31) + var3) * var3)) {
            read var4;
        }
    } else {
        read var5;
    }
}
procedure proc3 {
    read var6;
}
procedure proc4 {
    read var7;
    var3 = 69 * (var4 + ((68)));
}
procedure proc5 {
    read var8;
}
```

formatted.in:
```
"procedure proc1 {\n"
"    read var1;\n" // 1
"}\n"
"procedure proc2 {\n"
"    read var2;\n" // 2
"    if (16 != (var2)) then {\n" // 3
"        read var3;\n" // 4
"        while ((18 + var1) == 100 * (((var3 + 31) + var3) * var3)) {\n" // 5
"            read var4;\n" // 6
"        }\n"
"    } else {\n"
"        read var5;\n" // 7
"    }\n"
"}\n"
"procedure proc3 {\n"
"    read var6;\n" // 8
"}\n"
"procedure proc4 {\n"
"    read var7;\n" // 9
"    var3 = 69 * (var4 + ((68)));\n" // 10
"}\n"
"procedure proc5 {\n"
"    read var8;\n" // 11
"}\n"
