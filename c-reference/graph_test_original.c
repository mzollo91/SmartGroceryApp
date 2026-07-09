#include "graph.h"

int main(void)
{
    // create_graph check
    Graph *g = create_graph(5);
    if (g == NULL)
    {
        fprintf(stderr, "TEST FAILED: create_graph returned NULL\n");
        return 1;
    }
    printf("TEST PASSED: create_graph\n");

    // add_node check
    const char *locations[] = {"Entrance", "Dairy", "Produce", "Meat"};
    size_t locationsLength = sizeof(locations) / sizeof(locations[0]);

    for (size_t i = 0; i < locationsLength; i++)
    {
        bool ok = add_node(g, i + 1, locations[i]);
        if (!ok || g->nodeCount != i + 1)
        {
            fprintf(stderr, "TEST FAILED: add_node did not succeed as expected\n");
            free_graph(g);
            return 1;
        }
    }
    printf("TEST PASSED: add_node\n");

    // get_node_ptr check
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
            fprintf(stderr, "TEST FAILED: get_node_ptr grabbed an existing node.\n");
        }
        free_graph(g);
        return 1;
    }
    printf("TEST PASSED: get_node_ptr\n");

    // add_edge check

    // Node info array (2x4), row 0 is for ID1, row 1 is ID2.
    int nodeInfo[2][4] = {
        {1, 3, 4, 2}, // Row 0
        {3, 2, 1, 1}, // Row 1
    };

    // Corresponding distance array (1x4) to be paired with node info.
    float distances[1][4] = {
        {20, 16.5, 13, 9},
    };

    for (int i = 0; i < 4; i++)
    {
        int id1 = nodeInfo[0][i];
        int id2 = nodeInfo[1][i];
        float distance = distances[0][i];

        bool ok = add_edge(g, id1, id2, distance);

        if (!ok)
        {
            fprintf(stderr, "TEST FAILED: add_edge did not succeed as expected\n");
            free_graph(g);
            return 1;
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
            free_graph(g);
            return 1;
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
            free_graph(g);
            return 1;
        }
    }
    printf("TEST PASSED: add_edge\n");

    // print_graph check
    print_graph(g);
    free_graph(g);

    // Graph capacity check test
    Graph *g2 = create_graph(2);

    for (size_t i = 0; i < locationsLength; i++)
    {
        bool ok = add_node(g2, i + 1, locations[i]);
        if (!ok && g2->nodeCount == g2->capacity)
        {
            printf("TEST PASSED: capacity check.\n");
            break;
        }
        else if (ok && g2->nodeCount > g2->capacity)
        {
            fprintf(stderr, "TEST FAILED: add_node succeeded when graph capacity was exceeded.\n");
            free_graph(g2);
            return 1;
        }
        else if (!ok && g2->nodeCount < g2->capacity)
        {
            fprintf(stderr, "TEST FAILED: add_node failed on a valid add during the capacity check.\n");
            free_graph(g2);
            return 1;
        }
    }

    printf("All tests passed!");
    free_graph(g2);
    return 0;
}
