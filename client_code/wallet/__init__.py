from ._anvil_designer import walletTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil import alert, get_open_form
import random

class wallet(walletTemplate):
    global  count
    def __init__(self, user=None, **properties):
        self.init_components(**properties)
        self.user = user
        
        self.label_1.text = f"Welcome to Green Gate Financial, {user['username']}"
        self.bank_details_visible = False
        self.label_bank_details_error = Label(text="", role="alert")
        self.label_bank_name.visible = False
        self.textbox_bank_name.visible = False
        self.label_account_number.visible = False
        self.textbox_account_number.visible = False
        self.label_ifsc_code.visible = False
        self.textbox_ifsc_code.visible = False
        self.label_bank_details_error.visible = False
        self.button_save_bank_details.visible = False
        self.label_3.visible=False
        self.label_4.visible=False
        self.label_5.visible=False
        self.text_box_1.visible=False
        self.text_box_2.visible=False
        self.drop_down_1.visible=False
       
    def button_add_bank_details_click_click(self, **event_args):
       # Toggle the visibility of bank details labels and textboxes
        self.bank_details_visible = not self.bank_details_visible
        self.label_bank_name.visible = self.bank_details_visible
        self.textbox_bank_name.visible = self.bank_details_visible
        self.label_account_number.visible = self.bank_details_visible
        self.textbox_account_number.visible = self.bank_details_visible
        self.label_ifsc_code.visible = self.bank_details_visible
        self.textbox_ifsc_code.visible = self.bank_details_visible
        self.button_save_bank_details.visible = self.bank_details_visible
        self.label_3.visible=self.bank_details_visible
        self.label_4.visible=self.bank_details_visible
        self.label_5.visible=self.bank_details_visible
        self.text_box_1.visible=self.bank_details_visible
        self.text_box_2.visible=self.bank_details_visible
        self.drop_down_1.visible=self.bank_details_visible
        
        self.label_bank_details_error.text = ""
       
    def button_save_bank_details_click(self, **event_args):
      bank_name = self.textbox_bank_name.text
      account_number = self.textbox_account_number.text
      ifsc_code = self.textbox_ifsc_code.text
      account_holder_name = self.text_box_1.text
      branch_name = self.text_box_2.text
      account_Type = self.drop_down_1.selected_value
      wallet3 = anvil.server.call('generate_unique_id', self.user['username'], self.user['phone'])
      
      if bank_name and account_number and ifsc_code and account_holder_name and branch_name and account_Type:
        # Save the bank details to the 'accounts' table
        
        new_account = app_tables.accounts.add_row(
            user= self.user['username'],
            casa=int(account_number), 
            e_wallet=wallet3,
            bank_name=bank_name, 
            ifsc_code=ifsc_code,
            account_holder_name = account_holder_name,
            branch_name = branch_name,
            account_Type = account_Type
        )
        new_acc = app_tables.currencies.add_row(
          user= self.user['username'],
          casa= int(account_number),
          e_wallet=wallet3
        )

        self.label_bank_details_error.text = "Bank details saved successfully."
      else:
        self.label_bank_details_error.text = "Please fill in all bank details."

      

    def link_1_click(self, **event_args):
      open_form('deposit',user = self.user)

    def link_9_click(self, **event_args):
      open_form('transfer',user= self.user)

    def link_10_click(self, **event_args):
      open_form('withdraw',user= self.user)
