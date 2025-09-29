# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from .prompt import SYSTEM_PROMPT
from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from .tools.tools import get_sales_specials, get_service_specials, get_ev_incentives, get_vehicle_inventory_electric,get_vehicle_inventory_gas, get_service_content

# def context_callback(callback_context: CallbackContext):
#     callback_context.state["scraped_content"] = get_ev_incentives()
#     return get_ev_incentives()
root_agent = Agent(
   # A unique name for the agent.
   name="google_search_agent",
   # The Large Language Model (LLM) that agent will use.
   model="gemini-2.0-flash-live-001", # if this model does not work, try below
   #model="gemini-2.0-flash-live-001",
   # A short description of the agent's purpose.
   description="Agent to answer questions using tools.",
   # Instructions to set the agent's behavior.
   instruction=SYSTEM_PROMPT,
   # Add google_search tool to perform grounding with Google search.
   tools=[get_ev_incentives, get_sales_specials,get_service_content,get_service_specials,get_vehicle_inventory_electric,get_vehicle_inventory_gas],
    # before_model_callback=context_callback,
)
