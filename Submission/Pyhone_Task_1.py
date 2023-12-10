
import pandas as pd


def generate_car_matrix(df)->pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    # Write your logic here
  
    car = pd.read_csv('dataset-1.csv')
    car = car.pivot(index='id_1', columns='id_2', values='car')
    for i in range(min(car.shape[0], car.shape[1])):
        car.iloc[i, i] = 0
    return car

Sample result dataframe:
id_2   X  Y  Z
id_1           
A      0 10  0
B      3  0  8
C      0  2  7



def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here

    df = pd.read_csv('dataset-1.csv')
    df['car_type'] = pd.cut(df['car'], bins=[-float('inf'), 15, 25, float('inf')],
                            labels=['low', 'medium', 'high'], right=False)
    count = df['car_type'].value_counts().to_dict()
    count = dict(sorted(count.items()))

    return count()


def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here
  
    df = pd.read_csv('dataset-1.csv')
    b_mean = df['bus'].mean()
    bus_list = df[df['bus'] > 2 * b_mean].index.tolist()
    bus_list.sort()
  
    return bus_list()


def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here
  
    df = pd.read_csv('dataset-1.csv')
    avg_truck = df.groupby('route')['truck'].mean()
    routes = avg_truck[avg_truck > 7].index.tolist()
    routes.sort()

    return routes()


def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here
    
    new_matrix = matrix.copy()
    new_matrix = new_matrix.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)
    new_matrix = new_matrix.round(1)
  
    return new_matrix
id_2    X     Y    Z
id_1                
A      0.0  7.5  0.0
B      3.8  0.0  6.0
C      0.0  1.5  5.3

Sample result dataframe:


def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here
      
    df = pd.read_csv('dataset-1.csv')
    df['start_datetime'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'])
    df['end_datetime'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'])
    timemask = ((df['start_datetime'].dt.time != pd.Timestamp('00:00:00').time()) |
                 (df['end_datetime'].dt.time != pd.Timestamp('23:59:59').time()) |
                 (df['start_datetime'].dt.day_name() != 'Monday') |
                 (df['end_datetime'].dt.day_name() != 'Sunday'))
    series = df[timemask].set_index(['id', 'id_2']).index.duplicated(keep='first')
    return pd.Series()
