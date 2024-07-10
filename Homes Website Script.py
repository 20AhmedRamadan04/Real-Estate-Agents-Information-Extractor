from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as BE
import csv

header_written = False

location = input("Enter The Needed Location To Search For Homes Like (san-diego-ca): ")

for i in range(1, 16):
  browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
  browser.get(f"https://www.homes.com/real-estate-agents/{location}/p{i}")

  def main():
    src = browser.page_source
    soup = BE(src, "lxml")
    agents_details = []
    all_agents = soup.find("section", {"class": "asrp-container"}).find_all("li", {"class": "agent-results-item"})

    def get_agent_info(agent):
      agent_info = {}
      agent_name = agent.find("p", {"class": "agent-name"})
      agent_company = agent.find("p", {"class": "company"})
      agent_phone = agent.find("p", {"class": "phone"})
      agent_total_sales = agent.find("p", {"class": "total-sales"})
      agent_deals_area = agent.find("p", {"class": "deals-area"})
      agent_price_range = agent.find("p", {"class": "price-range"})

      if agent_name:
        agent_info["Agent Name"] = agent_name.text.strip()
      if agent_company:
        agent_info["Company"] = agent_company.text.strip()
      if agent_phone:
        agent_info["Phone"] = agent_phone.text.strip()
      if agent_total_sales:
        agent_info["Total Sales"] = agent_total_sales.text.strip()
      if agent_deals_area:
        agent_info["Deals Area"] = agent_deals_area.text.strip()
      if agent_price_range:
        agent_info["Price Range"] = agent_price_range.text.strip()

      return agent_info

    for agent in all_agents:
      agent_info = get_agent_info(agent)

      if agent_info:
        agents_details.append(agent_info)
    return agents_details
    
  agents_details = main()

  if agents_details:
    keys = agents_details[0].keys()
    with open(f'Homes website Real Estate Agents Info at {location}.csv', 'a', newline='') as output_file:
      dict_writer = csv.DictWriter(output_file, keys)
      if not header_written:
        dict_writer.writeheader()
        header_written = True
      dict_writer.writerows(agents_details)
  
  if i == 15:
    print("File Created")

  browser.quit()