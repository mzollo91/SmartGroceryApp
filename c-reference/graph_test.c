#include "graph.h"

// create_graph check
bool test_create_graph(Graph *g)
{
    if (g == NULL)
    {
        fprintf(stderr, "TEST FAILED: create_graph returned NULL\n");
        return false;
    }
    printf("TEST PASSED: create_graph\n");
    return true;
}

// add_node check
bool test_add_node(Graph *g, const char *locations[], size_t locationsLength)
{
    for (size_t i = 0; i < locationsLength; i++)
    {
        bool ok = add_node(g, i + 1, locations[i]);
        if (!ok || g->nodeCount != i + 1)
        {
            fprintf(stderr, "TEST FAILED: add_node did not succeed as expected\n");
            return false;
        }
    }
    printf("TEST PASSED: add_node\n");
    return true;
}

// get_node_ptr check
bool test_get_node_ptr(Graph *g)
{
    Node *n1 = get_node_ptr(g, 1);
    Node *n2 = get_node_ptr(g, 7);

    if (n1 == NULL || n2 != NULL)
    {
        if (n1 == NULL)
        {
            fprintf(stderr, "TEST FAILED: get_node_ptr failed to grab an existing node\n");
        }
        if (n2 != NULL)
        {
            fprintf(stderr, "TEST FAILED: get_node_ptr grabbed a existing node for an ID that doesn't exist.\n");
        }
        return false;
    }
    printf("TEST PASSED: get_node_ptr\n");
    return true;
}

// add_edge check
bool test_add_edge(Graph *g, int nodeInfo[2][4], float distances[1][4], int edgeCount)
{
    for (int i = 0; i < edgeCount; i++)
    {
        int id1 = nodeInfo[0][i];
        int id2 = nodeInfo[1][i];
        float distance = distances[0][i];

        bool ok = add_edge(g, id1, id2, distance);

        if (!ok)
        {
            fprintf(stderr, "TEST FAILED: add_edge did not succeed as expected\n");
            return false;
        }

        Node *n1 = get_node_ptr(g, id1);
        Node *n2 = get_node_ptr(g, id2);

        Edge *head1 = n1->head;
        Edge *head2 = n2->head;

        // Node head assigment check
        if (head1 == NULL || head2 == NULL)
        {
            if (head1 == NULL)
            {
                fprintf(stderr, "TEST FAILED: edge not assigned to n1->head.\n");
            }
            if (head2 == NULL)
            {
                fprintf(stderr, "TEST FAILED: edge not assigned to n2->head.\n");
            }
            return false;
        }

        // Node neighborID check
        if (head1->neighborID != id2 || head2->neighborID != id1)
        {
            if (head1->neighborID != id2)
            {
                fprintf(stderr, "TEST FAILED: Edge 1 neighborID mismatch, expected %d, got %d.\n", id2, head1->neighborID);
            }
            if (head2->neighborID != id1)
            {
                fprintf(stderr, "TEST FAILED: Edge 2 neighborID mismatch, expected %d, got %d.\n", id1, head2->neighborID);
            }
            return false;
        }
    }
    printf("TEST PASSED: add_edge\n");
    return true;
}

// Graph capacity check test
bool test_capacity(Graph *g2, const char *locations[], size_t locationsLength)
{
    for (size_t i = 0; i < locationsLength; i++)
    {
        bool ok = add_node(g2, i + 1, locations[i]);
        if (!ok && g2->nodeCount == g2->capacity)
        {
            printf("TEST PASSED: capacity check.\n");
            return true;
        }
        else if (ok && g2->nodeCount > g2->capacity)
        {
            fprintf(stderr, "TEST FAILED: add_node succeeded when graph capacity was exceeded.\n");
            return false;
        }
        else if (!ok && g2->nodeCount < g2->capacity)
        {
            fprintf(stderr, "TEST FAILED: add_node failed on a valid add during the capacity check.\n");
            return false;
        }
    }
    // Defensive fallback: only reachable if locationsLength <= capacity, meaning the
    // capacity boundary was never actually exercised. Not currently possible given the
    // data below, but returning false here (rather than falling through as a silent pass)
    // makes that gap visible instead of hidden.
    fprintf(stderr, "TEST FAILED: capacity limit was never reached during the check.\n");
    return false;
}

// cleanup: unlike free_graph (which assumes a valid, fully-formed graph and will crash
// on misuse by design), cleanup's job is to be a safe catch-all across every exit path --
// including the case where create_graph itself returned NULL. Hence the guard here.
void cleanup(Graph *g)
{
    if (g != NULL)
    {
        free_graph(g);
    }
}

int main(void)
{
    Graph *g = create_graph(5);

    if (!test_create_graph(g))
    {
        cleanup(g);
        return 1;
    }

    const char *locations[] = {"Entrance", "Dairy", "Produce", "Meat"};
    size_t locationsLength = sizeof(locations) / sizeof(locations[0]);

    if (!test_add_node(g, locations, locationsLength))
    {
        cleanup(g);
        return 1;
    }

    if (!test_get_node_ptr(g))
    {
        cleanup(g);
        return 1;
    }

    // Node info array (2x4), row 0 is for ID1, row 1 is ID2.
    int nodeInfo[2][4] = {
        {1, 3, 4, 2}, // Row 0
        {3, 2, 1, 1}, // Row 1
    };

    // Corresponding distance array (1x4) to be paired with node info.
    float distances[1][4] = {
        {20, 16.5, 13, 9},
    };

    if (!test_add_edge(g, nodeInfo, distances, 4))
    {
        cleanup(g);
        return 1;
    }

    // print_graph check
    print_graph(g);
    cleanup(g);

    Graph *g2 = create_graph(3);

    if (!test_capacity(g2, locations, locationsLength))
    {
        cleanup(g2);
        return 1;
    }

    printf("All tests passed!");
    cleanup(g2);
    return 0;
}