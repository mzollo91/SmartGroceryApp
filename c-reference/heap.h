// Start with guards.
#ifndef BINARY_HEAP
#define BINARY_HEAP

// Include dependencies, if any.
#include <stdio.h>
#include <stdbool.h>

// Define constants/macros, if any.

// Custom data types (Enums and Structs)
typedef struct
{
    float key; // Since this is to be used with Djikstra, it needs to be a float to be consistent with the data type being used for distance.
    int node_id;
} HeapNode;

typedef struct
{
    int nodeCount; // Naming convention kept consistent with graph.h.
    size_t capacity;
    int *position;   // Using a pointer here since C only allows for one flexible member per struct. The array will be fixed of capacity + 1 and sized once at runtime. The 0 index is unused to match with the numbering scheme of ID.
    HeapNode *nodes; // nodes will have a fixed size of capacity, indexing starting at 0.
} MinHeap;           // The heap data structure.

// Shared global variables (extern)

// Function pointers
MinHeap *create_min_heap(size_t capacity);
void free_min_heap(MinHeap *mh);

// Function prototypes
void swap(MinHeap *mh, int i, int j);

// End of Include Guard
#endif