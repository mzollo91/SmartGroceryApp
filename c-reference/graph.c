#include "graph.h"

Graph *create_graph(size_t capacity)
{
    Graph *g = malloc(sizeof(Graph));

    if (g == NULL)
    {
        // Use fprintf instead of printf. printf uses 'stdout' which is the standard output. fprintf can use
        // 'stderr' which is specifically for diagnostics.
        fprintf(stderr, "Malloc Error: %s\n", "graph failed to initialize.");
        return NULL;
    }

    g->capacity = capacity; // Since graph returns a pointer (Graph*), use '->' to set values to variables. Else, use '.'.
    g->nodeCount = 0;
    g->nodeArr = malloc(sizeof(Node) * capacity);
    if (g->nodeArr == NULL)
    {
        fprintf(stderr, "Malloc Error: %s\n", "node failed to initialize.");
        free(g);
        return NULL;
    }

    return g;
}