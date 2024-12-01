"""
Automate some basic AD/LDAP Queries
Author: Ryan Schanzenbacher

Requirements: ldap3
"""

from ldap3 import Server, Connection, SUBTREE, ALL_ATTRIBUTES
import json
from datetime import datetime, timedelta
import time
import random

class ADQuery:
    def __init__(self, server_address, domain, username, password):
        """
        Initialize AD Query with server details and credentials
        """

        self.server_address = server_address
        self.domain = domain
        self.username = f"{username}@{domain}"
        self.password = password
        self.base_dn = ','.join([f'DC={x}' for x in domain.split('.')])
        
    def connect(self):
        """
        Establish connection to AD server
        """

        try:
            server = Server(self.server_address, get_info=ALL_ATTRIBUTES)
            self.conn = Connection(
                server,
                user=self.username,
                password=self.password,
                auto_bind=True
            )
            return True
        except Exception as e:
            print(f"Connection failed: {str(e)}")
            return False

    def get_all_users(self):
        """
        Retrieve all users from Active Directory
        """

        try:
            search_filter = '(&(objectClass=user)(objectCategory=person))'
            attributes = ['displayName', 'mail', 'sAMAccountName', 'department', 'title']
            
            self.conn.search(
                search_base=self.base_dn,
                search_filter=search_filter,
                search_scope=SUBTREE,
                attributes=attributes
            )
            
            users = []
            for entry in self.conn.entries:
                user = {
                    'display_name': entry.displayName.value if hasattr(entry, 'displayName') else None,
                    'email': entry.mail.value if hasattr(entry, 'mail') else None,
                    'username': entry.sAMAccountName.value if hasattr(entry, 'sAMAccountName') else None,
                    'department': entry.department.value if hasattr(entry, 'department') else None,
                    'title': entry.title.value if hasattr(entry, 'title') else None
                }
                users.append(user)
                
            return users
            
        except Exception as e:
            print(f"Error retrieving users: {str(e)}")
            return []

    def get_user_details(self, username):
        """
        Get information for a specific user
        """

        try:
            search_filter = f'(&(objectClass=user)(objectCategory=person)(sAMAccountName={username}))'
            attributes = [
                'displayName', 'mail', 'sAMAccountName', 'department', 'title',
                'telephoneNumber', 'mobile', 'manager', 'whenCreated', 'lastLogon',
                'memberOf', 'company', 'physicalDeliveryOfficeName'
            ]
            
            self.conn.search(
                search_base=self.base_dn,
                search_filter=search_filter,
                search_scope=SUBTREE,
                attributes=attributes
            )
            
            if len(self.conn.entries) == 0:
                return None
                
            entry = self.conn.entries[0]

            # Some details we could want
            user_details = {
                'display_name': entry.displayName.value if hasattr(entry, 'displayName') else None,
                'email': entry.mail.value if hasattr(entry, 'mail') else None,
                'username': entry.sAMAccountName.value if hasattr(entry, 'sAMAccountName') else None,
                'department': entry.department.value if hasattr(entry, 'department') else None,
                'title': entry.title.value if hasattr(entry, 'title') else None,
                'phone': entry.telephoneNumber.value if hasattr(entry, 'telephoneNumber') else None,
                'mobile': entry.mobile.value if hasattr(entry, 'mobile') else None,
                'manager': entry.manager.value if hasattr(entry, 'manager') else None,
                'created_date': entry.whenCreated.value if hasattr(entry, 'whenCreated') else None,
                'last_logon': entry.lastLogon.value if hasattr(entry, 'lastLogon') else None,
                'groups': entry.memberOf.values if hasattr(entry, 'memberOf') else None,
                'company': entry.company.value if hasattr(entry, 'company') else None,
                'office': entry.physicalDeliveryOfficeName.value if hasattr(entry, 'physicalDeliveryOfficeName') else None
            }
            
            return user_details
            
        except Exception as e:
            print(f"Error retrieving user details: {str(e)}")
            return None

def runner(action):
    server_address = "ldap://group03.com"
    domain = "group03.com"
    username = "Administrator"
    password = "SuperS3curePW!"
    
    ad_query = ADQuery(server_address, domain, username, password)
    
    if ad_query.connect():
        if action[0] == "QUERY_ALL":
            # Get all users
            users = ad_query.get_all_users()
            return users
        
        elif action[0] == "QUERY_USER":
            # Get specific user details
            username = action[1]
            user_details = ad_query.get_user_details(username)
            if user_details:
                print(f"\nDetails for user {username}:")
                print(json.dumps(user_details, indent=2))
            else:
                print(f"\nUser {username} not found")
    
def main():
    """
    Main loop
    """
    end_time = datetime.now() + timedelta(hours=24)
    actions = ["QUERY_ALL","QUERY_USER"]
    users_known = []
    
    print("Beginning execution loop!")
    while datetime.now() < end_time:
        # Perform a random lookup, either entire tree or specific
        # user. Unless users are unknown (fresh start)
        if not users_known:
            # populate initial users
            print("Populating initial userlist")
            users_known = runner(("QUERY_ALL",))
            print(f"Initialized {len(users_known)} users...")
            wait_for = random.randint(5,15) * 60
            print(f"Sleeping for {wait_for} seconds")
            time.sleep(wait_for)
            continue

        # Random choices start here
        action = random.choice(actions)
        if action == "QUERY_ALL":
            print(f"Querying userlist...")
            users_known = runner(("QUERY_ALL",))

        elif action == "QUERY_USER":
            user = random.choice(users_known)['username']
            print(f"Running QUERY_USER for {user}")
            runner(("QUERY_USER",user))

        wait_for = random.randint(5,15) * 60
        print(f"Sleeping for {wait_for} seconds")
        time.sleep(wait_for)

if __name__ == "__main__":
    main()
