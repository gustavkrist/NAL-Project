import csv
from .load_config import load_config

def actor_significance(
	community : list,
	primary_column: str = "rotten_tomatoes_link",
	on_column: str = "actors",
	on_file: str = "rotten_tomatoes_movies.csv",
	config_path: str = ""
) -> dict:
	config = load_config(config_path)
	count = dict()
	with open(config["data_location"] + on_file) as csv_file:
		rotten_tomatoes = csv.reader(csv_file, delimiter=",", quotechar='"')
		for i, line in enumerate(rotten_tomatoes):
			if not i:
				head = line
			else:
				lookup = dict(zip(head, line))
				if lookup[primary_column] not in community:
					continue
				actors = lookup[on_column].strip().split(", ")
				already_counted = set()
				for actor in actors:
					if not actor in already_counted:
						if actor in count.keys():
							count[actor] += 1
						else:
							count[actor] = 1
						already_counted.add(actor)
	return count

def actor_reflection(
	community : list,
	name : str,
	primary_column: str = "rotten_tomatoes_link",
	on_column: str = "actors",
	on_file: str = "rotten_tomatoes_movies.csv",
	config_path: str = ""
) -> dict:
	config = load_config(config_path)
	count = dict()
	in_com_movies = 0
	all_movie = 0
	with open(config["data_location"] + on_file) as csv_file:
		rotten_tomatoes = csv.reader(csv_file, delimiter=",", quotechar='"')
		for i, line in enumerate(rotten_tomatoes):
			if not i:
				head = line
			else:
				lookup = dict(zip(head, line))
				actors = lookup[on_column].strip().split(", ")
				if lookup[primary_column] not in community and name in actors:
					all_movie += 1
				elif name in actors:
					all_movie += 1
					in_com_movies += 1
				else:
					continue
	return (in_com_movies, all_movie)


# see arguments for actor_significance
def get_most_significant_actor(*args, **kwargs) -> list:
	actors = actor_significance(*args, **kwargs)
	sig = max(actors.values())
	return ([actor for actor, v in actors.items() if  v==sig], sig)

