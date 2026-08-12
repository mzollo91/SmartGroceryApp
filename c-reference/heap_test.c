#include "heap.h"

// Test Functions
bool test_create_minheap(MinHeap *mh)
{
    if (mh == NULL)
    {
        fprintf(stderr, "TEST FAILED: create_min_heap returned NULL\n");
        return false;
    }
    printf("TEST PASSED: create_min_heap\n");
    return true;
}

bool test_insert(MinHeap *mh, int node_ids[], float keys[])
{

    // ID Range Check
    bool ok = insert(mh, node_ids[3], keys[3]);
    if (ok)
    {
        fprintf(stderr, "TEST FAILED: an ID out of bounds was able to be inserted.\n");
        return false;
    }
    ok = insert(mh, 0, 15.0);
    if (ok)
    {
        fprintf(stderr, "TEST FAILED: an ID of 0 was able to be inserted.\n");
        return false;
    }

    // Valid Data Insert Check
    for (size_t i = 0; i < mh->capacity; i++) // 'i' is size_t here to match the data type of capacity.
    {
        ok = insert(mh, node_ids[i], keys[i]);
        if (!ok)
        {
            fprintf(stderr, "TEST FAILED: valid data was not able to be inserted into the heap.\n");
            return false;
        }

        // Duplicate ID Check - runs only on the first iteration of the loop. This needs to be tested before the graph is at capacity.
        if (i == 0)
        {
            ok = insert(mh, node_ids[i], keys[i]);
            if (ok)
            {
                fprintf(stderr, "TEST FAILED: a duplicate ID was inserted into the heap.\n");
                return false;
            }
        }
    }

    // Capacity Check
    ok = insert(mh, node_ids[3], keys[3]); // Even though this is the same as the ID Range Check, the min heap is now at capacity. A capacity check is the first of the guards and will trigger first.
    if (ok)
    {
        fprintf(stderr, "TEST FAILED: capacity was exceeded in the min heap.\n");
        return false;
    }

    // Ordering check
    int correct_id_order[] = {2, 3, 1};
    for (size_t i = 0; i < mh->capacity; i++)
    {
        if (mh->nodes[i].node_id != correct_id_order[i])
        {
            fprintf(stderr, "TEST FAILED: nodes not inserted in the correct order. At index i = %zu, node_id was %d but should be %d.\n", i, mh->nodes[i].node_id, correct_id_order[i]);
            return false;
        }
    }

    printf("TEST PASSED: insert\n");
    return true;
}

// Main & Cleanup
void cleanup(MinHeap *mh)
{
    if (mh != NULL)
    {
        free_min_heap(mh);
    }
}

int main(void)
{
    MinHeap *mh = create_min_heap(3);

    if (!test_create_minheap(mh))
    {
        cleanup(mh);
        return 1;
    }

    int node_ids[] = {3, 1, 2, 4};
    // Correct ordering should be 2, 1, and 3, based on how the swap logic works (min heaps are not ordered, only the minimum value should be on the top).
    // The last ID, 4, is deliberately placed in there for a capacity check.

    float keys[] = {20.0, 15.1, 13.7, 19.8};

    if (!test_insert(mh, node_ids, keys))
    {
        cleanup(mh);
        return 1;
    }

    printf("All tests passed!");
    cleanup(mh);
    return 0;

    // Valgrind commands:
    // wsl - Activate wsl.
    // wsl --shutdown - Shutdown if needed for http proxy commands. Restart after.
    // gcc -g -Wall -o heap_test heap.c heap_test.c - Complile debug symbols and warnings.
    // valgrind --leak-check=full --show-leak-kinds=all --track-origins=yes ./heap_test - Run Valgrind
}