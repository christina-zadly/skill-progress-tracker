import sqlite3
class SkillsManager:
    """Manages skill tracking and progress stored in an SQLite database."""
    def __init__(self,db_path="skill-progress-tracker.db"):
        self.db = sqlite3.connect(db_path)
        self.cursor = self.db.cursor()
        self._create_table()
        self.user_id = None
    def _create_table(self):
        """Internal helper to ensure the database schema exists."""
        create_t = "CREATE TABLE IF NOT EXISTS Skills(User_id INTEGER, Skill TEXT, progress INTEGER)"
        self.cursor.execute(create_t)
        self.db.commit()
    def set_user(self, user_id):
        """Set the active user ID for all database operations."""
        self.user_id = user_id
    def find_skill(self, skill_name):
        """Get a skill name and check whether it exists for the current user."""
        find_s="select Skill from Skills where Skill=? and User_id=?"
        self.cursor.execute(find_s, (skill_name, self.user_id))
        return self.cursor.fetchone() is not None
    def show_all_skills(self):
        """Display all recorded skills and progress for the active user."""
        show_s="select Skill,progress from skills where user_id=?"
        self.cursor.execute(show_s,(self.user_id,))
        result = self.cursor.fetchall()
        print(f"You have {len(result)} Skills.")
        if result:
            print("Showing Skills With Progress: ")
            for skill, progress in result:
                print(f"Skill => {skill} Progress => {progress}%")
    def add_skill(self,skill_name, progress):
        """Add a new skill for the active user."""
        add_s = "INSERT INTO Skills(Skill, Progress, User_id) VALUES(?, ?, ?)"
        self.cursor.execute(add_s, (skill_name, progress, self.user_id))
        self.db.commit()
        print("Skill added successfully.")
    def update_skill(self, skill_name, progress):
        """Update progress for an existing skill."""
        if not self.find_skill(skill_name):
            print(f'Skill "{skill_name}" does not exist.')
            return False
        updat_s = "UPDATE Skills SET Progress=? WHERE Skill=? AND User_id=?"
        self.cursor.execute(updat_s, (progress, skill_name, self.user_id))
        self.db.commit()
        print("Progress updated successfully.")
        return True

    def delete_skill(self, skill_name):
        """Remove a skill for the active user."""
        if not self.find_skill(skill_name):
            print(f'Skill "{skill_name}" does not exist.')
            return False
        delete_s = "DELETE FROM Skills WHERE Skill=? AND User_id=?"
        self.cursor.execute(delete_s, (skill_name, self.user_id))
        self.db.commit()
        print("Skill deleted successfully.")
        return True
    def close(self):
        """Safely close the database connection."""
        self.db.close()
        print("Database connection closed.")
def get_integer_input(prompt, min_val=None, max_val=None):
    """Fetch an integer within optional min/max limits."""
    while True:
        try:
            val = int(input(prompt).strip())
            if min_val is not None and val < min_val:
                print(f"Value must be at least {min_val}.")
                continue
            if max_val is not None and val > max_val:
                print(f"Value must be at most {max_val}.")
                continue
            return val
        except ValueError:
            print("Invalid input! Please enter a valid number.")
       
def main():
    app = SkillsManager()
    user_id = get_integer_input("Input user ID: ")
    app.set_user(user_id)
    input_message = """
What do you want to do?
"s" => Show All Skills
"a" => Add a Skill
"d" => Delete a Skill
"u" => Update a Skill
"q" => Quit The App
Choose Option: """
    while True:
        user_input=input(input_message).strip().lower()

        if user_input =='s':
            app.show_all_skills()
        elif user_input == 'a':
            skill = input("Write the Skill : ").strip().capitalize()
            if app.find_skill(skill):
                print("Skill already exists.")
                up = input("Do you want to update the progress? (y/n): ").lower()
                if up == 'y':
                    prog = get_integer_input("Enter new progress: ",min_val=0, max_val=100)
                    app.update_skill(skill, prog)
            else:
                prog = get_integer_input("Enter the progress: ",min_val=0, max_val=100)
                app.add_skill(skill, prog)
                
        elif user_input == 'd':
            skill = input("Write the Skill name: ").strip().capitalize()
            app.delete_skill(skill)

            
        elif user_input == 'u':
            skill = input("Write the Skill name: ").strip().capitalize()
            prog = get_integer_input("Enter the new progress: ",min_val=0, max_val=100)
            app.update_skill(skill, prog)
        elif user_input == 'q':
            app.close()
            print("Goodbye!")
            break
        else:
            print(f'The option "{user_input}" was not found.')
if __name__ == "__main__":
    main()




