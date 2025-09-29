from .prompt import SYSTEM_PROMPT
from google.adk.agents import Agent
from .tools.tools import get_sales_specials, get_service_specials, get_ev_incentives, get_vehicle_inventory_electric,get_vehicle_inventory_gas, get_service_content

root_agent = Agent(
   name="voice_agent",
   model="gemini-2.0-flash-live-001",
   description="Agent to answer questions using tools.",
   instruction=SYSTEM_PROMPT,.
   tools=[get_ev_incentives, get_sales_specials,get_service_content,get_service_specials,get_vehicle_inventory_electric,get_vehicle_inventory_gas],
)

