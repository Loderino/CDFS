from utils.aggregation import mean_method, max_pool_method, min_pool_method, median_pooling, sum_method

NAME_TO_FUNC = {
            "mean": mean_method,
            "max": max_pool_method,
            "min": min_pool_method,
            "median": median_pooling,
            "sum": sum_method
        }