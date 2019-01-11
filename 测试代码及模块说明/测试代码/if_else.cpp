//²âÊÔif-elseÂß¼­µÄ²âÊÔ´úÂë 
#define A /********/ "asdas"/********///sdasdasda
#ifndef B
    #define B 2
    #ifdef C
        #define C 3
        #ifndef C
            #define C 5
        #endif
        #ifdef C
            #undef C
        #endif
    #else
        #ifdef C
            #define C 2
            #ifdef B
                #define Test1 10
            #else
                #define Test2 20
            #endif
        #else
            #define C 5
        #endif
        #ifdef C
            #define C 3
        #else
            #define C 5
        #endif
        #define D 1
    #endif
#endif
#define E 5
