import csv

def validate(edgelist,
    primary_column: str = "rotten_tomatoes_link",
    on_column: str = "actors",
    ratings_column: str = "tomatometer_rating",
    on_file: str = "rotten_tomatoes_movies.csv",
    data_location: str = "data/extracted/"
) -> None:
    head = []
    movies = dict()
    with open(data_location + on_file) as csv_file:
        rotten_tomatoes = csv.reader(csv_file, delimiter=",", quotechar='"')
        for i, line in enumerate(rotten_tomatoes):
            if not i:
                head = line
            else:
                lookup = dict(zip(head, line))
                movies[lookup[primary_column]] = [set(lookup[on_column].strip().split(", ")), int(lookup[ratings_column] if lookup[ratings_column] else 0)]
    for movie in edgelist:
        for connection in edgelist[movie]:
            assert(movies[movie][0].intersection(movies[connection][0]))
            assert(abs(movies[movie][1] - movies[connection][1]) == edgelist[movie][connection]['weight'])