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

void free_graph(Graph *g)
{
    // Use nodeCount for the loop as this is incremented for each node
    for (int i = 0; i < g->nodeCount; i++)
    {
        Node *n = &g->nodeArr[i]; // Use the '&' symbol here to point to the memory address of the node in the array.
        Edge *current = n->head;
        while (current != NULL)
        {
            Edge *temp = current->next;
            free(current);
            current = temp;
        }
    }
    // since the memory is allocated for the entire array,
    // it must be freed the same way rather than by individual node.
    free(g->nodeArr);
    free(g);
}
