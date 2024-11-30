import requests
import pprint
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.list import MDListItem, MDListItemHeadlineText
#from kivy.uix.accordion import Accordion, AccordionItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFabButton

# Designate Our .kv design file 
Builder.load_file('box.kv')


global data_price_unique
global data
data = []
data_price_unique = []


######### Get the api response ############
def first_tier(item_name):  ## get a list of items with unique products 
	global data
	global data_price_unique
	parameters = {
		"ItemName": item_name
	}
	response = requests.get("https://script.google.com/macros/s/AKfycbyMst1biNF1MXOZCkEhAS7cbmVM4qEwhQbziT7oPVmXZgZ_FGzRYDgenCNpAP2ovWU7/exec", params=parameters)
	response.raise_for_status()
	data = response.json()['data']
	#pprint.pprint(response.json()['data'])
	data_price_unique = list({item["Price"]:item for item in data}.values())
	#pprint.pprint(data_price_unique	)
	return data_price_unique


def second_tier(item_name, price):
		discount_data = [ d for d in data if d['Price'] == price]
		#pprint.pprint(discount_data)
		MyLayout().add_item_2(item_name=item_name ,discount_data=discount_data)
		#print(item_name)


####### data populated from json response
class Listitem(MDListItem): # create list items
	
	def item_press(self):
		#global item_name
		#global price
		item_name =  self.ids.label1.text
		if "%" not in item_name: # check if there are items in accordion 1
			#print(item_name)
			price = item_name.rsplit(':', 1)[-1]
			#print(price)
			#print(item_name)
			second_tier(item_name, price)
			#return item_name
		else:
			pass		
	
######### main Layout ################
class MyLayout(Widget):

	
	def add_item(self):
		global data_price_unique

		self.ids.container_1.clear_widgets() #clear items in accordion 2


		self.ids.title1.title = self.ids.name.text  # change accordion 2 title
		self.ids.title1.collapse = False   # expand the accordion 2 
		self.ids.label2.text = "Searching"

		item_name = self.ids.name.text
		first_tier(item_name=item_name)

		if len(data_price_unique) == 0: #### if there is no product 
			self.ids.label2.text = "No product found"
		else:
			for n in range(len(data_price_unique)):	  # loop to extract data 
				item = Listitem()
				self.ids.container_1.add_widget(item)
				#print(data_price_unique[n]['ItemName'])
				item.ids.label1.text = f"product name: {data_price_unique[n]['ItemName']}            \
								price:{data_price_unique[n]['Price'] }"
				n += 1
		
		#self.ids.title1.collapse = False   # expand the accordion 2 

	def add_item_2(self, item_name, discount_data):  ## populate Accordion 1
		app = App.get_running_app()
		# for n in range(len(data_price_unique)):	
		# 	self.remove_widget(item)
		app.root.ids.container_2.clear_widgets() #clear items in accordion 1
		
		for n in range(len(discount_data)):
			item = Listitem()
			app.root.ids.container_2.add_widget(item) 
			item.ids.label1.text = f"product name: {discount_data[n]['ItemName']}   \
			 Store: {discount_data[n]['Store']}   \
			 Discount:   {discount_data[n]['Discount'] } %"
			n += 1 

		app.root.ids.title_product.title = item_name
		app.root.ids.title_product.collapse = False ## expand accordion 1
		
		#print(item_name)
		#print(self.ids.title_product)
		#print(AccordionItem.ids.<kivy.uix.accordion.AccordionItem)


class MaestroApp(MDApp):
	dialog = None
	
	def build(self):
		#Clock.schedule_once(self.add_item_2)
		return MyLayout()
		

	
	
if __name__ == '__main__':
	MaestroApp().run()