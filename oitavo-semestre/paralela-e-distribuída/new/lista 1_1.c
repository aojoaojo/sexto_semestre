#include <stdio.h>

#define TAMANHO 1000

void sum_vectors(int *vetor1, int *vetor2, int *resultado, int tamanho)
{
    for (int i = 0; i < tamanho; i++)
    {
        resultado[i] = vetor1[i] + vetor2[i];
    }
}

int main()
{
    int vetor1[TAMANHO];
    int vetor2[TAMANHO];
    int resultado[TAMANHO];

    for (int i = 0; i < TAMANHO; i++)
    {
        vetor1[i] = i + 1;
        vetor2[i] = (i + 1) * 2;
    }

    sum_vectors(vetor1, vetor2, resultado, TAMANHO);

    printf("Soma dos vetores (primeiros 10 elementos):\n");
        printf("resultado[%d] = %d\n", i, resultado[i]);

    printf("Soma dos vetores (últimos 10 elementos):\n");
    for (int i = TAMANHO - 10; i < TAMANHO; i++)
    {
        printf("resultado[%d] = %d\n", i, resultado[i]);
    }

    return 0;
}
