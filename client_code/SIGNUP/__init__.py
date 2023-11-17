from ._anvil_designer import SIGNUPTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class SIGNUP(SIGNUPTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.server.call(
      'add_info', 
      self.text_box_1.text, 
      self.text_box_2.text, 
      self.text_box_3.text,
      self.text_box_4.text
    )
    alert (self.text_box_1.text + ' added')
    open_form('LOGIN')

