#include "graph.h"

int main(void)
{
    Graph *g = create_graph(5);
    if (g == NULL)
    {
        fprintf(stderr, "TEST FAILED: create_graph returned NULL\n");
        return 1;
    }

    bool ok = add_node(g, 1, "Entrance");
    if (!ok || g->nodeCount != 1)
    {
        fprintf(stderr, "TEST FAILED: add_node did not succeed as expected\n");
        free_graph(g);
        return 1;
    }

    printf("TEST PASSED: create_graph + add_node\n");

    free_graph(g);
    return 0;
}