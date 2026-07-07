// Start with guards.
#ifndef ADJACENCY_LIST
#define ADJACENCY_LIST

// Include dependencies, if any.
#include <stdio.h>
#include <stdbool.h>

// Define constants/macros, if any.

// Custom data types (Enums and Structs)

typedef struct Edge
{ // 'Edge' is the typedef tag name, needed for self referencing structs.
	int neighborID;
	float distance;
	struct Edge *next;
} Edge; // typedef alias

typedef struct
{
	int id;
	char aisleName[20];
	Edge *head; // 'struct' is not needed here as Edge will be fully built before Node.
} Node;

typedef struct
{
	int nodeCount;
	size_t capacity;
	Node *nodeArr;
} Graph;

// Shared global variables (extern)

// Function pointers
Graph *create_graph(size_t capacity);
void free_graph(Graph *g);

// Function prototypes
bool add_node(Graph *g, int id, const char name[]);
bool add_edge(Graph *g, int id1, int id2, float distance); // printf to be used in the source file for specific messages, such as duplicate errors.
Node *get_node_ptr(Graph *g, int id);
void print_graph(Graph *g); // pointer to graph so function doesn't make a copy of it.

// End of Include Guard
#endif