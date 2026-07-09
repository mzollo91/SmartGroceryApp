#include "graph.h"
#include <string.h>
#include <stdlib.h>

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

    if (get_node_ptr(g, id) != NULL) // The rule of thumb: '&' is for turning a value into a pointer.
    {
        fprintf(stderr, "Add Node Error: %s\n", "Node ID already exists.");
        return false;
    }

    n->id = id;

    // Cap strncopy to limit the number of characters to the size of n->aisleName - 1 to leave room for the \0 null terminator.
    strncpy(n->aisleName, name, sizeof(n->aisleName) - 1);
    n->aisleName[sizeof(n->aisleName) - 1] = '\0'; // force the last character to be '\0'

    n->head = NULL;

    g->nodeCount++;
    return true;
}

Node *get_node_ptr(Graph *g, int id)
{
    for (int i = 0; i < g->nodeCount; i++)
    {
        Node *n = &g->nodeArr[i];
        if (id == n->id)
        {
            return n;
        }
    }
    return NULL;
}

bool add_edge(Graph *g, int id1, int id2, float distance)
{
    Node *n1 = get_node_ptr(g, id1);
    Node *n2 = get_node_ptr(g, id2);

    if (n1 == NULL || n2 == NULL)
    {
        if (n1 == NULL)
        {
            fprintf(stderr, "Node Error: %s\n", "Node 1 ID not found.");
        }
        if (n2 == NULL)
        {
            fprintf(stderr, "Node Error: %s\n", "Node 2 ID not found.");
        }
        return false;
    }

    Edge *aToB = malloc(sizeof(Edge));
    Edge *bToA = malloc(sizeof(Edge));

    if (aToB == NULL || bToA == NULL)
    {
        if (aToB == NULL)
        {
            fprintf(stderr, "Edge Error: %s\n", "Malloc call failed for Edge A->B.");
        }
        if (bToA == NULL)
        {
            fprintf(stderr, "Edge Error: %s\n", "Malloc call failed for Edge B->A.");
        }
        free(aToB); // Free both regardless of which is NULL, since free() can't fail if the pointer is null.
        free(bToA);
        return false;
    }

    aToB->distance = distance;
    aToB->neighborID = id2;
    aToB->next = n1->head; // 1: new edge points at whatever head currently is
    n1->head = aToB;       // 2: head now points at the new edge

    bToA->distance = distance;
    bToA->neighborID = id1;
    bToA->next = n2->head;
    n2->head = bToA;

    return true;
}

void print_graph(Graph *g)
{
    for (int i = 0; i < g->nodeCount; i++)
    {
        Node *n = &g->nodeArr[i];
        Edge *current = n->head;
        printf("Edge neighbor IDs and distances for Node ID %d:\n", n->id);
        while (current != NULL)
        {
            printf("Neighbor ID: %d\n Distance(ft): %.2f\n", current->neighborID, current->distance);
            current = current->next;
        }
    }
}