
from database import create_table, get_all_applications

create_table()

print("Database created successfully!")

applications = get_all_applications()

print("\nExisting Applications:")
print(applications)
