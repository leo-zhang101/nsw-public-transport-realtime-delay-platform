# nsw-public-transport-realtime-delay-platform
End-to-end data engineering platform for monitoring real-time public transport delays in NSW using GTFS feeds, AWS data lake, and analytics stack.


## NSW Public Transport Delay Analytics

This project builds an end-to-end data pipeline for analysing real-time delays in NSW public transport using GTFS static and GTFS realtime data.

### Key Outputs
- Route-level delay KPIs 
- Stop-level delay KPIs
- Enriched trip-level delay fact table

###  Example Output 

| route_id     | route_short_name | avg_delay_sec | max_delay_sec | events |
|-------------|------------------|---------------|---------------|--------|
| 1-10M-sj2-2 | 10M              | 30            | 120           | 2      |

### Observations

- Route 10M shows an average delay of 30 seconds, with peak delays reaching 120 seconds
- Delay events are concentrated at major interchange stops such as Central Station
- This suggests congestion impact during peak interchange periods
