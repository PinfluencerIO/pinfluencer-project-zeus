#todo move to logging
def print_exception(e):
    print(''.join(['Exception ', str(type(e))]))
    print(''.join(['Exception ', str(e)]))