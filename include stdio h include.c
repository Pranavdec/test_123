#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <stdbool.h>
#include <math.h>
#include <unistd.h>
bool is_prime(int n)
{
    if (n <= 1)
    {
        return false;
    }
    int i;
    for (i = 2; i <= sqrt(n); i++)
    {
        if (n % i == 0)
        {
            return false;
        }
    }
    return true;
}
int main()
{
    sleep(20);
    clock_t start, end;
    double time_taken;
    double tot_time = 0.0;
    int i, j;
    int intervals[10] = {1000000, 2000000, 3000000, 4000000,
                         5000000, 6000000, 7000000, 8000000, 9000000, 10000000};
    for (i = 0; i < 10; i++)
    {
        printf("Interval (%d, %d)\n", 1, intervals[i]);
        start = clock();
        for (j = 2; j <= intervals[i]; j++)
        {
            if (is_prime(j))
            {
                // printf("%d ", j);
            }
        }
        end = clock();
        time_taken = ((double)(end - start)) / CLOCKS_PER_SEC;
        tot_time += time_taken;
    }
    printf("\nTotal Time Taken: %.2f seconds\n", tot_time);
    sleep(20);
    return 0;
}
