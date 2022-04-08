#include "generate_id.h"

using namespace std;

string generate_id() {
    string chars(CHARS);
    string id(ID_SIZE,' ');
    for (int i = 0; i < ID_SIZE; i++)
	    id[i] = chars[rand() % chars.size()];
    return id;
}

