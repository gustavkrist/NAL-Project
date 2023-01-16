from nal import basic_statistics, load_graph, plot_degree_distribution

G = load_graph() 
plot_degree_distribution(G, 'out/degree-distribution')
basic_statistics(G, format='latex', filename="out/statistics")