def response_converter(status, message, serialized_data):
    """
        Convert response data into a standardized format.

        Args:
            status (str): The status of the response (e.g., 'success', 'error').
            message (str): A message providing additional information about the response.
            serialized_data (dict): The data to be included in the response.

        Returns:
            dict: A dictionary containing the status, message, and data of the response.
    """
    return {
        'status': status,
        'message': message,
        'data': serialized_data
    }
