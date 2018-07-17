# Dissolver, 
a tiny task chunking command line tool.

Project updates at https://medium.com/@Apoc.

## INSTALLATION:
personally I've aliased it in ~/.bashrc

## USAGE:
dissolve [INSTRUCTION [INPUT]]

### INSTRUCTIONS:
>help 
>
>shows this help message

>goal
>
>shows list of goals

>problem
>
>shows list of problems

### INPUTS
>(goal) "your input"
>
>switches to and creates new "your input.dat" goal datfile

>(goal) del "your input"
>
>deletes your current problem and defaults to default.dat

>(problem) "your input"
>
>deletes "your input" subproblem

>(problem) "your input" "other input"
>
>creates new subproblem "other input" under "your input"
