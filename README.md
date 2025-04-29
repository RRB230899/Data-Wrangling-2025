# Data Wrangling Course Project - Rutgers University, New Brunswick - Spring 2025

## TITLE: Impact of Earthquakes on Semiconductor Supply Chain Resilience for Server Manufacturing in Taiwan
### Team Members:
- Raghav Bajaj
- Mithil Kadam
- Raunak Nair

### WHY?
- Taiwan is critical to the global semiconductor supply chain (TSMC, UMC, ASE, etc.).
- Taiwan sits right on a dangerous seismic zone — the Philippine Sea Plate and Eurasian Plate boundary.
- Earthquakes directly disrupt fabs (fabrication plants), which are incredibly sensitive: even tiny tremors can cause millions of dollars in damage.
- Governments, investors, and supply chain managers obsess over this risk.
- Recent earthquakes (2024) have again raised alarms about resiliency and diversification of chip supply.
- TSMC is the only major company mass-producing at the 2nm level — or about to mass-produce.
- Their N2 process (that's their name for 2nm tech) is targeted for:
  + Early Risk Production: 2025
  + Volume Production: 2026
  + (They're sticking to this timeline despite some earthquake disruptions.)
- No one else — Intel, Samsung — is yet shipping true 2nm products.
  + Intel plans to launch Intel 20A (their 2nm equivalent) but... they've been struggling with execution and delays.
  + Samsung says 2nm is coming in 2025-2026, but their 3nm was bumpy already.

### Dataset
- Earthquake Data: USGS API
- Scraper: Bing News

### Modules used:
- BeautifulSoup
- Spacy
- nltk
- Requests
- Pandas
