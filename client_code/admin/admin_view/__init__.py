from ._anvil_designer import admin_viewTemplate
from anvil import alert, open_form
from anvil.tables import app_tables
import re

class admin_view(admin_viewTemplate):
    def __init__(self, user_data=None, **properties):
        self.init_components(**properties)
        self.edit_mode = False 
        self.text_box_8.visible = False
        self.text_box_10.visible = False
        self.text_box_9.visible = False
        self.text_box_11.visible = False
        self.text_box_12.visible = False

        self.label_9.visible = False
        self.label_10.visible = False
        self.label_11.visible = False
        self.label_12.visible = False
        self.label_13.visible = False
      
        


        # Initialize the dropdown with account numbers
        self.populate_account_dropdown(user_data)

        if user_data:
            # Any code you write here will run before the form opens.
            self.populate_textboxes(user_data)
            self.toggle_edit_mode()
          
        self.set_button_text()
          
    def set_button_text(self):
        username = self.text_box_1.text
        user = app_tables.users.get(username=username)

        if user is not None:
            # Check the current state of 'hold' column
            current_state = user['hold']

            # Set button text based on the current state
            self.button_5.text = "Unfreeze" if current_state else "Freeze"# Initial mode setup

    def populate_account_dropdown(self, user_data):
        # Get account numbers associated with the user from the 'accounts' table
        user_accounts = app_tables.accounts.search(user=user_data['username'])

        # Extract account numbers and populate the dropdown
        account_numbers = [str(account['casa']) for account in user_accounts]
        self.drop_down_1.items = account_numbers

    def button_2_click(self, **event_args):
    # Get the selected account number from the dropdown
       selected_account_number = float(self.drop_down_1.selected_value)

# Get the 'e_money' amount from the 'accounts' table
       account = app_tables.accounts.get(user=self.text_box_1.text, casa=selected_account_number)
      
      # Check if 'e_money' is not empty
       if account and account['e_money'] is not None and int(account['e_money']) > 0:
          user_to_delete = app_tables.users.get(username=self.text_box_1.text)
          if user_to_delete is not None:
            user_to_delete.update(banned=True)
            alert("User has some funds remaining.User added to banned list .", title="Error")
          return
  
      # Check if currency values are not empty
       currency_details = app_tables.currencies.get(casa=float(selected_account_number))

       if currency_details and (
          currency_details['money_usd'] is not None and float(currency_details['money_usd']) > 0 or
          currency_details['money_inr'] is not None and float(currency_details['money_inr']) > 0 or
          currency_details['money_euro'] is not None and float(currency_details['money_euro']) > 0 or
          currency_details['money_swis'] is not None and float(currency_details['money_swis']) > 0
        ):
          user_to_delete = app_tables.users.get(username=self.text_box_1.text)
          if user_to_delete is not None:
            user_to_delete.update(banned=True)
            alert("User has some funds remaining.User added to banned list.", title="Error")
          return
   
      # If 'e_money' and currency values are empty, proceed with user deletion
       username = self.text_box_1.text
       user_to_delete = app_tables.users.get(username=username)
  
       if user_to_delete is not None:
              # Delete user from 'users' table
              user_to_delete.delete()
      
              # Delete user's accounts from 'accounts' table
              accounts_to_delete = app_tables.accounts.search(user=username)
              for account in accounts_to_delete:
                  account.delete()
      
              # Delete user's currencies from 'currencies' table
              currencies_to_delete = app_tables.currencies.search(user=username)
              for currency in currencies_to_delete:
                  currency.delete()
      
              alert("User and associated information deleted successfully.", title="Success")
      
              # Clear textboxes after deletion
              self.clear_textboxes()
      
              # Raise an event to notify the parent form (admin form) about the deletion
              open_form('admin', user_data=user_to_delete)

  
    def clear_textboxes(self):
        self.text_box_1.text = ''
        self.text_box_2.text = ''
        self.text_box_3.text = ''
        self.text_box_4.text = ''
        self.text_box_5.text = ''
        self.text_box_6.text = ''
        self.text_box_7.text = ''
        self.text_box_12.text = ''  # Clear text_box_12

    def populate_textboxes(self, user_data):
        self.text_box_1.text = user_data['username']
        self.text_box_2.text = user_data['email']
        self.text_box_3.text = user_data['password']
        self.text_box_4.text = user_data['phone']
        self.text_box_5.text = user_data['aadhar']
        self.text_box_6.text = user_data['pan']
        self.text_box_7.text = user_data['address']

    def toggle_edit_mode(self):
        # Toggle between view and edit modes
        self.edit_mode = not self.edit_mode
        self.text_box_1.enabled = self.edit_mode
        self.text_box_2.enabled = self.edit_mode
        self.text_box_3.enabled = self.edit_mode
        self.text_box_4.enabled = self.edit_mode
        self.text_box_5.enabled = False  # Aadhar (not editable during edit mode)
        self.text_box_6.enabled = False  # Pan (not editable during edit mode)
        self.text_box_7.enabled = self.edit_mode
        self.drop_down_1.enabled = self.edit_mode  # Enable/disable dropdown based on the mode

        # Change button_1 text based on the mode
        self.button_1.text = 'Save Changes' if self.edit_mode else 'Edit'

    def is_valid_phone(self, phone):
        # Check if the phone number is not empty and has exactly 10 digits
        return bool(phone and re.match(r'^\d{10}$', str(phone)))

    def button_1_click(self, **event_args):
        if self.edit_mode:
            # Validate phone number
            if not self.is_valid_phone(self.text_box_4.text):
                alert("Please enter a valid 10-digit phone number.", title="Error")
                return

            # Save changes to the database
            username = self.text_box_1.text
            user_to_update = app_tables.users.get(username=username)

            if user_to_update is not None:
                user_to_update.update(
                    email=self.text_box_2.text,
                    password=self.text_box_3.text,
                    phone=self.text_box_4.text,
                    aadhar=self.text_box_5.text,
                    pan=self.text_box_6.text,
                    address=self.text_box_7.text
                )

                alert("Changes saved successfully.", title="Success")

                # Toggle back to view mode after saving changes
                self.toggle_edit_mode()
        else:
            # Toggle to edit mode
            self.toggle_edit_mode()

    def button_3_click(self, **event_args):
        open_form('admin.show_users')

    def button_4_click(self, **event_args):
        # Get the selected account number from the dropdown
        selected_account_number = self.drop_down_1.selected_value

        if selected_account_number is not None:
            # Get the 'e_money' amount from the 'accounts' table
            account = app_tables.accounts.get(user=self.text_box_1.text, casa=int(selected_account_number))
            if account is not None:
                # Display 'e_money' in text_box_12
                self.text_box_12.text = str(account['e_money'])
  
                # Get the currency details from the 'currencies' table
                currency_details = app_tables.currencies.get(casa=int(selected_account_number))
  
                if currency_details is not None:
                    # Display currency details in respective textboxes and labels
                    self.text_box_8.text = str(currency_details['money_usd'])
                    self.text_box_10.text = str(currency_details['money_inr'])
                    self.text_box_9.text = str(currency_details['money_euro'])
                    self.text_box_11.text = str(currency_details['money_swis'])
  
                    # Set the visibility of text boxes and labels to True
                    self.text_box_8.visible = True
                    self.text_box_10.visible = True
                    self.text_box_9.visible = True
                    self.text_box_11.visible = True
                    self.text_box_12.visible = True

                    # Set the visibility of labels to True
                    self.label_9.visible = True
                    self.label_10.visible = True
                    self.label_11.visible = True
                    self.label_12.visible = True
                    self.label_13.visible = True

    def button_5_click(self, **event_args):
        username = self.text_box_1.text
        user_to_update = app_tables.users.get(username=username)

        if user_to_update is not None:
            # Check the current state of 'hold' column
            current_state = user_to_update['hold']

            # If 'hold' is None or 'true', user is considered frozen, otherwise unfrozen
            new_state = not current_state

            # Update the 'hold' column in the 'users' table
            user_to_update.update(hold=new_state if new_state else None)

            # Update button text based on the new state
            self.button_5.text = "Unfreeze" if new_state else "Freeze"

            # Display alert based on the action
            alert_message = "User is frozen." if new_state else "User is unfrozen."
            alert(alert_message, title="Status")
