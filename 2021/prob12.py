from collections import defaultdict

S, E = 'start', 'end'
with open('data/prob12.dat') as f:
    graph = defaultdict(set)
    visit = defaultdict(lambda: 0)

    def add_edge(n, m):
        if not m == S:
            graph[n].add(m)
        if n.isupper():
            visit[n] = -float('inf')

    for line in f.readlines():
        A, B = line.strip().split('-')
        add_edge(A, B)
        add_edge(B, A)

    def count_paths(C, uses_double):
        if C == E:
            return 1

        ans = 0
        visit[C] += 1
        for N in graph[C]:
            if visit[N] <= 0:
                ans += count_paths(N, uses_double)
            elif not uses_double:
                ans += count_paths(N, uses_double=True)
        visit[C] -= 1
        return ans

    print(count_paths(S, uses_double=False))

