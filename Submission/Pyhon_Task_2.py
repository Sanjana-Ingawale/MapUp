import pandas as pd


def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # Write your logic here
    df = pd.read_csv(dataset-3.csv)
    distance_matrix = pd.DataFrame(index=df['id'].unique(), columns=df['id'].unique())
    distance_matrix = distance_matrix.fillna(0)
  
    for _, row in df.iterrows():
        source_id = row['source_id']
        destination_id = row['destination_id']
        distance = row['distance']

        distance_matrix.loc[source_id, destination_id] += distance

    distance_matrix = distance_matrix + distance_matrix.T - pd.DataFrame(np.diag(distance_matrix))

    return distance_matrix
Sample result dataframe:
     A  B   C
  A  0 10   8
  B 10  0   5
  C  8  5   0


def unroll_distance_matrix(df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Write your logic here
    import pandas as pd

    def unroll_distance_matrix(input_matrix):

    unrolled_df = pd.DataFrame(columns=['id_start', 'id_end', 'distance'])

    for id_start in input_matrix.index:
        for id_end in input_matrix.columns:
            # Exclude same id_start to id_end combinations
            if id_start != id_end:
                distance = input_matrix.loc[id_start, id_end]
                unrolled_df = unrolled_df.append({'id_start': id_start, 'id_end': id_end, 'distance': distance}, ignore_index=True)

    return unrolled_df


def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    # Write your logic here
    
    reference_df = input_df[input_df['id_start'] == reference_value]
    avg_distance = reference_df['distance'].mean()
    threshold_lower = 0.9 * avg_distance
    threshold_upper = 1.1 * avg_distance
    result_ids = input_df[(input_df['distance'] >= threshold_lower) & (input_df['distance'] <= threshold_upper)]['id_start'].unique()
    result_ids.sort()
    return result_ids


def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Wrie your logic here
    df_with_rates = input_df.copy()
    rate_coefficients = {'moto': 0.8, 'car': 1.2, 'rv': 1.5, 'bus': 2.2, 'truck': 3.6}
    for vehicle_type, rate_coefficient in rate_coefficients.items():
        column_name = f'{vehicle_type}_rate'
        df_with_rates[column_name] = df_with_rates['distance'] * rate_coefficient
    return df_with_rates

Sample result dataframe:
     id_start id_end  distance  moto_rate  car_rate  rv_rate  bus_rate  truck_rate
0        A      B        10        8.0      12.0     15.0      22.0        36.0
1        A      C         8        6.4       9.6     12.0      17.6        28.8
2        B      A        10        8.0      12.0     15.0      22.0        36.0
3        B      C         5        4.0       6.0      7.5      11.0        18.0
4        C      A         8        6.4       9.6     12.0      17.6        28.8
5        C      B         5        4.0       6.0      7.5      11.0        18.0



def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Write your logic here
    df_with_time_rates = input_df.copy()

    time_ranges = [(time(0, 0, 0), time(10, 0, 0)),
                   (time(10, 0, 1), time(18, 0, 0)),
                   (time(18, 0, 1), time(23, 59, 59))]

    weekday_discount_factors = [0.8, 1.2, 0.8]
    weekend_discount_factor = 0.7

    for start_time, end_time in time_ranges:
        weekday_mask = (df_with_time_rates['start_time'].dt.time >= start_time) & \
                       (df_with_time_rates['start_time'].dt.time <= end_time) & \
                       (df_with_time_rates['start_day'].isin(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']))
        df_with_time_rates.loc[weekday_mask, 'weekday_discount'] = weekday_discount_factors[time_ranges.index((start_time, end_time))]

        weekend_mask = (df_with_time_rates['start_time'].dt.time >= start_time) & \
                       (df_with_time_rates['start_time'].dt.time <= end_time) & \
                       (df_with_time_rates['start_day'].isin(['Saturday', 'Sunday']))
        df_with_time_rates.loc[weekend_mask, 'weekend_discount'] = weekend_discount_factor

    df_with_time_rates['weekday_discount'] = df_with_time_rates['weekday_discount'].fillna(1.0)
    df_with_time_rates['weekend_discount'] = df_with_time_rates['weekend_discount'].fillna(1.0)

    df_with_time_rates['weekday_discounted_rate'] = df_with_time_rates['distance'] * df_with_time_rates['weekday_discount']
    df_with_time_rates['weekend_discounted_rate'] = df_with_time_rates['distance'] * df_with_time_rates['weekend_discount']

    return df_with_time_rates
  
Sample result dataframe:
   id_start id_end  start_day start_time end_day  end_time  distance  weekday_discount  weekend_discount  weekday_discounted_rate  weekend_discounted_rate
0        A      B     Monday   08:30:00  Monday   09:30:00        10               0.8               0.7                      8.0                     7.0
1        A      B     Monday   12:00:00  Monday   14:00:00        15               1.2               0.7                     18.0                    10.5
2        A      B     Monday   19:00:00  Monday   20:30:00        20               0.8               0.7                     16.0                    14.0
3        A      B  Wednesday   08:30:00  Wednesday  09:30:00        10               0.8               0.7                      8.0                     7.0
4        A      B  Wednesday   12:00:00  Wednesday  14:00:00        15               1.2               0.7                     18.0                    10.5
5        A      B  Wednesday   19:00:00  Wednesday  20:30:00        20               0.8               0.7                     16.0                    14.0
