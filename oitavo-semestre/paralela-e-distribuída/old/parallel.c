#include <stdlib.h>
#include <stdio.h>
#include <omp.h>

int randomize_vector(int *v, int n)
{
    for (int i = 0; i < n; i++)
    {
        // v[i] = rand() % 100;
        v[i] = i;
    }
    return 0;
}

void main()
{
    int n[1000];
    int m[1000];
    randomize_vector(n, 1000);
    randomize_vector(m, 1000);

#pragma omp parallel for
    for (int i = 0; i < 1000; i++)
    {
        n[i] += m[i];
    }

    int soma_total = 0;

#pragma omp parallel for reduce(+ : soma_total)
    for (int i = 0; i < 1000; i++)
    {
        soma_total += n[i];
    }
    printf("Total sum: %d\n", soma_total);
    printf("\n");
}
