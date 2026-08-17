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

bool insert(MinHeap *mh, int node_id, float key)
{
    // Guards against exceeding capacity, node_id values out of bounds, and inserting duplicate nodes.
    if (mh->nodeCount == mh->capacity) // Since nodeCount can not be negative, it is safe to compare to capacity (a size_t datatype). If this is not guaranteed, a negative value guard must be used.
    {
        fprintf(stderr, "Insert Error: %s\n", "min heap is already at capacity.");
        return false;
    }
    if (node_id <= 0 || node_id > mh->capacity)
    {
        fprintf(stderr, "Insert Error: %s: %zu.\n", "node_id must fall between 0 and capacity", mh->capacity);
        return false;
    }
    if (mh->position[node_id] != -1)
    {
        fprintf(stderr, "Insert Error: %s\n", "node ID already exists in the heap.");
        return false;
    }

    // Create an initial new node and set its position.
    HeapNode *node = &mh->nodes[mh->nodeCount];
    node->node_id = node_id;
    node->key = key;
    mh->position[node_id] = mh->nodeCount;

    int parentIdx; // initialize the parent index variable.

    // Begin the sift up loop.
    // while (mh->position[node_id] > 0 && (parentIdx = (mh->position[node_id] - 1) / 2, mh->nodes[parentIdx].key > key)) - this is a less verbose version of the block below, but at not as straight forward to understand at a glance.
    while (mh->position[node_id] > 0)
    {
        parentIdx = (mh->position[node_id] - 1) / 2; // Parent index is defined as (i -1) / 2, ignoring the remainder.

        if (mh->nodes[parentIdx].key <= key)
        {
            break;
        }

        swap(mh, mh->position[node_id], parentIdx);
    }

    // Increase nodeCount after success of the function.
    mh->nodeCount++;

    return true;
}

bool extract_min(MinHeap *mh, HeapNode *minNode)
{
    // Check if the heap is empty first.
    if (mh->nodeCount == 0)
    {
        fprintf(stderr, "Extract Min Error: %s\n", "nodeCount is 0, there are no elements in the heap.");
        return false;
    }

    // Get the min node and reset its position to -1.
    *minNode = mh->nodes[0]; // dereference and copy, using "&" will reassign the pointer to minNode.

    // No need to replace the extracted node with an empty node, it will overwritten when a new node is inserted. The guards in the insert function are based on nodeCount which is decremented here.

    // Move the last element to the root.
    int leafNodeId = mh->nodes[mh->nodeCount - 1].node_id;
    int oldRootId = mh->nodes[0].node_id;

    swap(mh, mh->position[oldRootId], mh->position[leafNodeId]);
    int leafNodeIdx = mh->position[leafNodeId]; // In the case of 1 element heap, the leafNodeIdx and the old root index will be the same. Setting the position to -1 first would result in leafNodeIdx not having a real index value.
    mh->position[oldRootId] = -1;               // Set the position to the old root to -1 after the swap has been made. If done before, it can cause the new, valid root's position to be set to -1; indicating that is doesn't exist in the heap.

    mh->nodeCount--;

    // As a note, the index of the children of the sifted element are 2i+1 (left child) and 2i+2 (right child).
    // Sift down loop.
    while (true)
    {
        int smallestIdx = leafNodeIdx;

        int leftChildIdx = 2 * leafNodeIdx + 1;
        int rightChildIdx = 2 * leafNodeIdx + 2;

        if (leftChildIdx < mh->nodeCount) // Check to see if the child index is valid based on nodeCount.
        {
            float leftChild_key = mh->nodes[leftChildIdx].key;
            if (leftChild_key < mh->nodes[smallestIdx].key)
            {
                smallestIdx = leftChildIdx;
            }
        }

        if (rightChildIdx < mh->nodeCount) // Check to see if the child index is valid based on nodeCount.
        {
            float rightChild_key = mh->nodes[rightChildIdx].key;
            if (rightChild_key < mh->nodes[smallestIdx].key)
            {
                smallestIdx = rightChildIdx;
            }
        }

        if (smallestIdx == leafNodeIdx)
        {
            break;
        }

        swap(mh, smallestIdx, leafNodeIdx);
        leafNodeIdx = mh->position[leafNodeId];
    }
    return true;
}