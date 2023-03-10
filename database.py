import oracledb
import config
oracledb.init_oracle_client()


class DbInteract:
    def __init__(self, maximum_connections=2):
        self.connection_pool = oracledb.create_pool(user=config.database_user,
                                                    password=config.database_password,
                                                    host=config.database_host,
                                                    port=config.database_port,
                                                    service_name=config.database_service_name,
                                                    min=1,
                                                    max=maximum_connections,
                                                    increment=1)

    def run_query(self, sql, params=None):
        rows = None
        with self.connection_pool.acquire() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, params)
                rows = cursor.fetchall()
        return rows
    
    def execute_sql(self, sql, params=None):
        count = None
        with self.connection_pool.acquire() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, params)
                count = cursor.rowcount
                connection.commit()
        return count
    
    def close_connection_pool(self):
        self.connection_pool.close()
    

class ManageEmployee(DbInteract):   
    def get_employee(self, payroll_no):
        sql = "select * from employees where payroll_no = :payroll_no"
        results = self.run_query(sql, [payroll_no])
        return results
    
    def get_max_payroll_number(self):
        results = self.run_query("select max(payroll_no) from employees")
        return results[0][0]

    def insert_employee(self, surname, forename):
        sql = """
        insert into employees
        (payroll_no, date_created, user_created, flex_clock_id, start_date, ni_no, sex, date_of_birth, surname, forname, title)
        values
        (:payroll_no, CURRENT_DATE, USER, 1234, CURRENT_DATE, 'NN123456A', 'MALE', '01-DEC-2000', :surname, :forename, 'MR')
        """
        payroll_no = self.get_max_payroll_number() + 1
        rowcount =  self.execute_sql(sql, [payroll_no, surname, forename])
        return rowcount, payroll_no

    def delete_employee(self, payroll_no, safety=True):
        sql = """
        delete from employees 
        where 
        payroll_no = :payroll_no
        """
        if safety:
            sql = sql + "\n and user_created = USER"
        rowcount = self.execute_sql(sql, [payroll_no])
        return rowcount
    
    def update_employee(self, payroll_no, surname, safety=True):
        sql = """
        update employees
        set surname = :surname
        where
        payroll_no = :payroll_no
        """
        if safety:
            sql = sql + "\n and user_created = USER"
        rowcount = self.execute_sql(sql, [surname, payroll_no])
        return rowcount     


if __name__ == "__main__":
    mydb = ManageEmployee()
    # Create
    count, employee_id = mydb.insert_employee("TESTING", "TOAST")
    print("Created employee:", employee_id)
    # Read
    details = mydb.get_employee(employee_id)
    print(details)
    # Update
    count = mydb.update_employee(employee_id, "TOASTED")
    print("Updated:", count)
    # Read again
    details = mydb.get_employee(employee_id)
    print(details)
    # Delete
    count = mydb.delete_employee(employee_id)
    print("Deleted:", count)
    # Read yet again
    details = mydb.get_employee(employee_id)
    print("After deletion we have:", details)
    mydb.close_connection_pool()
