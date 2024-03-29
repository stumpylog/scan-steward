from pprint import pprint
import psutil
from humanize import naturalsize
import database.country
import database.subdivision

process = psutil.Process()
initial = process.memory_info()

print(dir(database))

x = database.country.get_country_by_code("DE")

country = process.memory_info()

pprint(list(x.subdivisions))

subdivision = process.memory_info()

print(f"Initial: {naturalsize(initial.rss)}")
print(f"Country: {naturalsize(country.rss)} ({naturalsize(country.rss - initial.rss)})")
print(
    f"Subdivision: {naturalsize(subdivision.rss)} ({naturalsize(subdivision.rss - country.rss)})"
)

print(database.subdivision.valid_subdivision_code("DE-BB"))
print(database.subdivision.valid_subdivision_code("DE-XX"))
print(database.subdivision.valid_subdivision_code("XX-BB"))

countries = list(
    [x for x in database.country.get_country_by_partial_name("Jordan", ratio=85.0)]
)
pprint(countries)
