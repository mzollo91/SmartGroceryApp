#include "heap.h"
#include <string.h>
#include <stdlib.h>

MinHeap *create_min_heap(size_t capacity)
{
    MinHeap *mh = malloc(sizeof(MinHeap));

    if (mh == NULL)
    {
        // Use fprintf instead of printf. printf uses 'stdout' which is the standard output. fprintf can use
        // 'stderr' which is specifically for diagnostics.
        fprintf(stderr, "Malloc Error: %s\n", "min heap failed to initialize.");
        return NULL;
    }

    mh->capacity = capacity; // Since min heap returns a pointer (MinHeap*), use '->' to set values to variables. Else, use '.'.
    mh->nodeCount = 0;
    mh->nodes = malloc(sizeof(HeapNode) * capacity);
    if (mh->nodes == NULL)
    {
        fprintf(stderr, "Malloc Error: %s\n", "node array failed to initialize.");
        free(mh);
        return NULL;
    }

    mh->position = malloc(sizeof(int) * (capacity + 1));
    if (mh->position == NULL)
    {
        fprintf(stderr, "Malloc Error: %s\n", "position array failed to initialize.");
        free(mh->nodes);
        free(mh);
        return NULL;
    }
    // Below, the sizing uses the same expression used for mh->position. Using sizeof(mh->position) does not actually size based on the position array, rather it sizes to the pointer itself (8 bytes on a 64 bit machine.)
    memset(mh->position, -1, sizeof(int) * (capacity + 1)); // An alternative to a for loop, fills a block of memory byte-by-byte. This method can be used for either a 0 or -1 int, but not other values.

    return mh;
}

void free_min_heap(MinHeap *mh)
{
    // Since the memory is allocated for the entire array,
    // it must be freed the same way rather than by individual node.
    free(mh->nodes);
    free(mh->position);
    free(mh);
}

void swap(MinHeap *mh, int i, int j)
{
    // Get node ids
    int n1 = mh->nodes[i].node_id;
    int n2 = mh->nodes[j].node_id;

    // Swap the nodes
    HeapNode tempNode = mh->nodes[i]; // Copy tempNode by value, if it points to the node's memory address then the value of tempNode will be also be overwritten in the next line.
    mh->nodes[i] = mh->nodes[j];
    mh->nodes[j] = tempNode;

    // Swap the positions
    int tempPos = mh->position[n1]; // Same reasoning as tempNode to copy by value.
    mh->position[n1] = mh->position[n2];
    mh->position[n2] = tempPos;
}