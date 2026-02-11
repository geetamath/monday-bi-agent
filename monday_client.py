import requests
import os

class MondayClient:
    def __init__(self):
        self.api_key = os.getenv('MONDAY_API_KEY')
        self.url = "https://api.monday.com/v2"
        self.headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json"
        }
    
    def get_board_data(self, board_id):
        """Fetch all items from a board"""
        query = f'''
        {{
            boards(ids: {board_id}) {{
                name
                items_page(limit: 500) {{
                    items {{
                        id
                        name
                        column_values {{
                            id
                            text
                            value
                        }}
                    }}
                }}
            }}
        }}
        '''
        
        try:
            response = requests.post(
                self.url,
                json={'query': query},
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def get_all_boards(self):
        """Get list of all boards"""
        query = '{ boards { id name } }'
        
        try:
            response = requests.post(
                self.url,
                json={'query': query},
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def get_all_boards_data(self):
        """Fetch data from both boards"""
        work_orders_id = os.getenv('WORK_ORDERS_BOARD_ID')
        deals_id = os.getenv('DEALS_BOARD_ID')
        
        if not work_orders_id or not deals_id:
            return {"error": "Board IDs not configured"}
        
        work_orders = self.get_board_data(work_orders_id)
        deals = self.get_board_data(deals_id)
        
        return {
            "work_orders": work_orders,
            "deals": deals
        }