# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookscarperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Strip all whitespoaces from strings
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != 'description':
                value = adapter.get(field_name)
                adapter[field_name] = value.strip()

        # Category & Product Type into lowercase
        lowercase_keys = ['category', 'product_type']
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            adapter[lowercase_key] = value.lower()

        # Convert price to float from string
        price_fields = ['price', 'price_excl_tax', 'price_incl_tax', 'tax']
        for price_field in price_fields:
            value = adapter.get(price_field)
            value = value.replace('£', '')
            adapter[price_field] = float(value)

        # Availability: Extract only number from string
        availability_string = adapter.get('availability')
        split_availability = availability_string.split('(')
        if len(split_availability) < 2:
            adapter['availability'] = 0
        else:
            availability_arr = split_availability[1].split(' ')
            adapter['availability'] = float(availability_arr[0])

        # Reviews: Convert number of reviews from string to int
        num_reviews = adapter.get('num_reviews')
        adapter['num_reviews'] = int(num_reviews)

        # Stars: Convert text to number
        stars = adapter.get('stars')
        star_text_value = stars.split(' ')[1]
        star_text_value = star_text_value.lower()
        if star_text_value == "zero":
            adapter['stars'] = 0
        elif star_text_value == "one":
            adapter['stars'] = 1
        elif star_text_value == "two":
            adapter['stars'] = 2
        elif star_text_value == "three":
            adapter['stars'] = 3
        elif star_text_value == "four":
            adapter['stars'] = 4
        elif star_text_value == "five":
            adapter['stars'] = 5

        return item
