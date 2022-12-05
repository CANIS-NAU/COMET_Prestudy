# Filters out all twitter posts that do not include some variation of the word "speed test"

NR == 1 || (($11~/[sS]peedtest/ || $11~/[Ss]peed [Tt]est/) && ($12 == "en")){print}
