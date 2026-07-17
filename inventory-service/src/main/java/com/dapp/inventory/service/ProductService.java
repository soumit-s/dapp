package com.dapp.inventory.service;

import org.springframework.stereotype.Service;

import com.dapp.inventory.model.Product;
import com.dapp.inventory.repository.ProductRepository;
import com.dapp.inventory.schema.ProductCreatedEventDto;
import com.dapp.inventory.schema.ProductCreatedEventPayloadDto;

@Service
public class ProductService {
    private final ProductRepository productRepository;

    public ProductService(ProductRepository productRepository) {
        this.productRepository = productRepository;
    }

    public void createProductFromKafkaEvent(ProductCreatedEventDto event) {
        ProductCreatedEventPayloadDto payload = event.getPaylaod();
        Product product = new Product();
        product.setId(payload.getId());
        product.setName(payload.getName());
        product.setDescription(payload.getDescription());

        productRepository.save(product);
    }
}
