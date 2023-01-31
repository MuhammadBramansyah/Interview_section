def get_employee():
    query = f""" 
        select * from empl.employees
    """
    return query

def get_history():
    query = f"""
        select * from hstr.history
    """
    return query