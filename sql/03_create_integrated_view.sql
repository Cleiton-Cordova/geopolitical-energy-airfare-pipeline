-- Create an integrated view of economic and geopolitical indicators
CREATE OR REPLACE VIEW public.vw_energy_airfare_geopolitical AS
SELECT
    e.date,
    e.country_code,
    e.country,
    e.airfare_index,
    e.price_usd_per_barrel,
    e.price_usd_per_gallon,
    g.conflict_events,
    g.avg_goldstein,
    g.total_mentions
FROM public.energy_airfare AS e
LEFT JOIN public.gdelt_monthly AS g
    ON e.date = g.month;