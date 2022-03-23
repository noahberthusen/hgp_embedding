//qcode.h
#define END_OF_FILE "-1"

//mat.h
#define DEBUG false
#define None -2

//decoder.cpp
#define STOP false


////////// Modify here //////////
/////////////////////////////////
/////////////////////////////////
//generator.h
#define weight_flag false
#define sampling_flag false

//main.cpp
#define flip_flag false
/////////////////////////////////
/////////////////////////////////
/////////////////////////////////


// write_resul.cpp
// Two physical probability will be considered the same when |p1 - p2| < EPSILON
#define EPSILON 0.000001


// generate_id.h
#define ID_SIZE 8
#define CHARS "0123456789abcdefghijklmnopqrstuvwxyz"

//main.cpp
#define DEFAULT_RES_FILE_NAME string("../results/cpp_laptop_") + generate_id() + ".res"
/* #define DEFAUT_CODE_FILE_NAME "ccode/swap_70_60_6_7.code" */
//true for flip + ssflip and false for direct ssflip
