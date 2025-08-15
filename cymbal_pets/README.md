# Cymbal Pets dataset

This dataset contains sample products for our pets.

## Installation

Create a dataset called `petverse` or modify the command below.
Use the following command to load the `AVRO` file into a new table in your dataset:

```sql
LOAD DATA INTO petverse.cymbal_pets
OPTIONS(
    description="Cymbal pets products table"
  )
FROM FILES (
  uris = ['gs://sample-data-and-media/cymbal-pets/tables/products/products_000000000000.avro'],
  format = 'avro'
);
```

## Licensing

* See [LICENSE](LICENSE) for code
* For dataset, media files (audio, video, images), [CC-0](https://creativecommons.org/public-domain/cc0/) applies