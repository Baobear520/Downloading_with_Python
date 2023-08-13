template_url = ("https://api.worldbank.org/v2/en/indicator/"
    "{resource}?downloadformat=csv"
)

urls = [
    # Total population by country
    template_url.format(resource="SP.POP.TOTL"),

     # GDP by country
    template_url.format(resource="NY.GDP.MKTP.CD"),

     # Population density by country
    template_url.format(resource="EN.POP.DNST"),
 ]