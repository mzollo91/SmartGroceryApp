#include "graph.h"
#include <string.h>

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

bool add_node(Graph *g, int id, const char name[])
{
    if (g->capacity <= g->nodeCount)
    {
        fprintf(stderr, "Add Node Error: %s\n", "nodeCount is equal to or greater than capacity");
        return false;
    }
    // There is no need to malloc a new node. The memory allocation already exists in the graph created.
    // Creating a new node will lead to a node allocated in memory that will never be used if g->nodeArr[g->nodeCount] = *n
    // is used. Using *n dereferences it, copying the whole struct by value.
    Node *n = &g->nodeArr[g->nodeCount];
    // Placeholder comment to add duplicate id check later.
    n->id = id;

    // Cap strncopy to limit the number of characters to the size of n->aisleName - 1 to leave room for the \0 null terminator.
    strncpy(n->aisleName, name, sizeof(n->aisleName) - 1);
    n->aisleName[sizeof(n->aisleName) - 1] = '\0'; // force the last character to be '\0'

    n->head = NULL;

    g->nodeCount++;
    return true;
}
