# Cymbal Pets dataset

This dataset contains sample products for our pets.

## Installation

Create a dataset called `petverse` or modify the command below.
Use the following commands to load the `AVRO` files into new tables in your dataset:

```sql
LOAD DATA INTO petverse.products
OPTIONS(
    description="Cymbal pets products table"
  )
FROM FILES (
  uris = ['gs://sample-data-and-media/cymbal-pets/tables/products/*.avro'],
  format = 'avro'
);

LOAD DATA INTO petverse.orders
OPTIONS(
    description="Cymbal pets orders table"
  )
FROM FILES (
  uris = ['gs://sample-data-and-media/cymbal-pets/tables/orders/*.avro'],
  format = 'avro'
);

LOAD DATA INTO petverse.order_items
OPTIONS(
    description="Cymbal pets order items table"
  )
FROM FILES (
  uris = ['gs://sample-data-and-media/cymbal-pets/tables/order_items/*.avro'],
  format = 'avro'
);

LOAD DATA INTO petverse.customers
OPTIONS(
    description="Cymbal pets customers table"
  )
FROM FILES (
  uris = ['gs://sample-data-and-media/cymbal-pets/tables/customers/*.avro'],
  format = 'avro'
);

```

## Licensing

* See [LICENSE](LICENSE) for code
* For dataset, media files (audio, video, images), [CC-0](https://creativecommons.org/public-domain/cc0/) applies