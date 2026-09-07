// Start with guards.
#ifndef DJIKSTRA_ALG
#define DJIKSTRA_ALG

// Include dependencies, if any.
#include <stdio.h>
#include <stdbool.h>

// Define constants/macros, if any.

// Custom data types (Enums and Structs)

typedef struct
{
    size_t capacity;
    float *dist; // Using a pointer here since C only allows for one flexible member per struct. The array will be sized once at runtime.
    int *prev;
} DjikstraResult;

// Shared global variables (extern)

// Function pointers
DjikstraResult *run_djikstra(size_t capacity);
void free_djikstra_result(DjikstraResult *dr);

// Function prototypes

// End of Include Guard
#endif