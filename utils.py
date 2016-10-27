def get_category(tweet):
	final_cat = []
	FILTERS = ['sports', 'politics', 'business', 'music', 'tech', 'health', 'finance', 'india', 'books', 'celebrity']
	for category in FILTERS:
		if category in tweet:
			final_cat.append(category)
	return final_cat


