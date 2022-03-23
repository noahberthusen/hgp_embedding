## Algorithms:

For the .res files, following parameterize the algorithm used

0 : bit flip on classical code (NOT AVAILABLE FOR CPP)

1 : small set flip where we divide by the weighted cardinality of the flip

2 : small set flip where we divide by the cardinality of the flip

3 : divide by the weighted cardinality + sampling of indices in gray code within the function score_gen

4 : divide by the cardinality + sampling of indices in gray code within the function score_gen

5 : flip + small set flip where we divide by the weighted cardinality of the flip

6 : flip + small set flip where we divide by the cardinality of the flip

7 : flip + divide by the weighted cardinality + sampling of indices in gray code within the function score_gen

8 : flip + divide by the cardinality + sampling of indices in gray code within the function score_gen


## Main program (C++)
To compile the decoder use

>       g++ -Wall -Wextra -Ofast main.cpp qcode.cpp decoder.cpp generator.cpp mat.cpp read_code.cpp -o test.out

Note that -O3 flag can also be used; there doesn't seem to be much of a difference between these flags.

To run the program use

>       ./test.out

For more info on optimization flags see 

1. [gnu.org](http://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html)
2. [stackoverflow](https://stackoverflow.com/questions/14492436/g-optimization-beyond-o3-ofast)

For further optimizations, use the Intel compiler instead of GCC/G++ (See [here](https://software.intel.com/en-us/parallel-studio-xe)).

## Main program (python)
To generate classical codes, use (-h to see available options):

>        python3 generate_codes.py

To compile the pyx file, use

>       cd src_py/; python3 setup.py build_ext --inplace; cd ..

This can then be called from within main.py

To run the decoder use

>        python3 main.py

To create one file with all the results use (-h to see available options):

>        python3 combine_results.py

To plot (-h to see available options):

>        python3 plot.py

### Profiling

To profile the code, use

>        python3 profile.py >> profile_decoder.txt

### Testing classical codes

In order to test classical codes using the flip algorithm, use

>       python3 flip.py