import { faker } from "@faker-js/faker";
import {writeFileSync} from 'fs';

var products = [];

for (let i = 0; i < 200; ++i) {
  products.push({
    name: faker.commerce.productName(),
    description: faker.commerce.productDescription(),
    price: faker.commerce.price(),
  });
}

const jsonString = JSON.stringify(products, null, 2);

writeFileSync("products.json", jsonString, "utf-8");
