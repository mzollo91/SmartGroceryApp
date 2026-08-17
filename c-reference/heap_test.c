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

        // Duplicate ID Check - runs only on the first iteration of the loop. This needs to be tested before the heap is at capacity.
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

bool test_extract_min(MinHeap *mh, HeapNode *minNode, MinHeap *emptyHeap)
{
    // Check the empty capacity guard/
    bool ok = extract_min(emptyHeap, minNode);
    if (ok)
    {
        fprintf(stderr, "TEST FAILED: extract_min was successful on an empty heap.\n");
        return false;
    }

    ok = extract_min(mh, minNode);
    if (!ok)
    {
        fprintf(stderr, "TEST FAILED: extract_min failed on a valid heap.\n");
        return false;
    }
    if (minNode->node_id != 2 || minNode->key != 13.7f)
    {
        fprintf(stderr, "TEST FAILED: extract_min failed to extract the minimum node. Got node_id = %d and key = %f, expected node_id = 2 and key = 13.7.\n", minNode->node_id, minNode->key);
        return false;
    }

    // Ordering check
    int correct_id_order[] = {1, 4, 3}; // After extracting the min (node ID 2), sift down should move node ID 3 to the root, and then perform a single swap with node ID 1. Node ID 3 does not have children at that point.
    for (int i = 0; i < mh->nodeCount; i++)
    {
        if (mh->nodes[i].node_id != correct_id_order[i])
        {
            fprintf(stderr, "TEST FAILED: sift down did not maintain the heap property. At index i = %d, node_id was %d but should be %d.\n", i, mh->nodes[i].node_id, correct_id_order[i]);
            return false;
        }
    }

    printf("TEST PASSED: extract_min\n");
    return true;
}

bool test_decrease_key(MinHeap *mh, int nodeId, float newKey)
{
    // Test ID bounds.
    bool ok = decrease_key(mh, 7, 21.0);
    if (ok)
    {
        fprintf(stderr, "TEST FAILED: key was decreased on a node ID out of bounds of the heap.\n");
        return false;
    }

    // Test nonexistent key.
    ok = decrease_key(mh, 5, 11.0);
    if (ok)
    {
        fprintf(stderr, "TEST FAILED: key was decreased on a node ID that does not exist in the heap.\n");
        return false;
    }

    // Test against increasing the key.
    ok = decrease_key(mh, nodeId, mh->nodes[mh->position[nodeId]].key + 2.0);
    if (ok)
    {
        fprintf(stderr, "TEST FAILED: key was increased.\n");
        return false;
    }

    // Test that the value and position updated.
    ok = decrease_key(mh, nodeId, newKey);
    if (!ok)
    {
        fprintf(stderr, "TEST FAILED: key was not decreased on a valid node ID.\n");
        return false;
    }
    if (mh->nodes[mh->position[nodeId]].key != newKey)
    {
        fprintf(stderr, "TEST FAILED: node id = %d's key was not updated to the new value. Current key is %f, expected %f.\n", nodeId, mh->nodes[mh->position[nodeId]].key, newKey);
        return false;
    }

    // Test the new order. Inserted order is [2, 4, 1, 3].
    int correct_id_order[] = {2, 3, 1, 4}; // After decreasing node ID 3's key from 20.0 -> 14.8, one swap should take place between node ID 4 and 3.
    for (int i = 0; i < mh->nodeCount; i++)
    {
        if (mh->nodes[i].node_id != correct_id_order[i])
        {
            fprintf(stderr, "TEST FAILED: sift up did not maintain the heap property. At index i = %d, node_id was %d but should be %d.\n", i, mh->nodes[i].node_id, correct_id_order[i]);
            return false;
        }
    }
    printf("TEST PASSED: test_decrease_key\n");
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
    // Correct ordering should be 2, 3, and 1, based on how the swap logic works (min heaps are not ordered, only the minimum value should be on the top).
    // The last ID, 4, is deliberately placed in there for a capacity check.

    float keys[] = {20.0, 15.1, 13.7, 19.8};

    if (!test_insert(mh, node_ids, keys))
    {
        cleanup(mh);
        return 1;
    }

    // Rebuild the Min Heap to contain all 4 nodes.
    cleanup(mh);
    mh = create_min_heap(4); // create_min_heap already proven to work at this point, no need to retest.
    for (size_t i = 0; i < mh->capacity; i++)
    {
        insert(mh, node_ids[i], keys[i]); // Insert test would have passed at this point, so using the same data should not cause any issues.
    }

    MinHeap *emptyHeap = create_min_heap(5);
    HeapNode minNode;

    if (!test_extract_min(mh, &minNode, emptyHeap))
    {
        cleanup(emptyHeap);
        cleanup(mh);
        return 1;
    }

    cleanup(emptyHeap);

    // Cleanup and rebuild the Min Heap to contain all 4 nodes.
    cleanup(mh);
    mh = create_min_heap(5);
    for (int i = 0; i < 4; i++) // A value of 4 is used here to prevent stack over read. Looping through to capacity. The fifth iteration (i = 4) would have input garbage bytes as node_ids[4] doesn't exist.
    {
        insert(mh, node_ids[i], keys[i]);
    }

    // For the decrease_key test, updating node ID 3 to a lower value.
    int updateNodeId = 3;
    float newKey = 14.8;

    if (!test_decrease_key(mh, updateNodeId, newKey))
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