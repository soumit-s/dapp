package com.dapp.inventory.listener;

import org.springframework.kafka.annotation.KafkaHandler;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.support.Acknowledgment;
import org.springframework.stereotype.Component;

import com.dapp.inventory.schema.ProductCreatedEventDto;
import com.dapp.inventory.service.ProductService;

@Component
@KafkaListener(id = "product-event-listener", groupId = "inventory-service-product-listener", topics = "outbox.product")
public class ProductEventListener {
    private final ProductService productService;

    public ProductEventListener(ProductService productService) {
        this.productService = productService;
    }

    @KafkaHandler
    public void handleProductCreatedEvent(ProductCreatedEventDto event, Acknowledgment ack) {
        System.out.printf("%d %s \n", event.getPaylaod().getId(), event.getPaylaod().getName());
        // TODO: Error handling. Dead letter queue.
        productService.createProductFromKafkaEvent(event);
    }

    @KafkaHandler(isDefault = true)
    public void handleUnknown(Object fallback, Acknowledgment ack) {
        System.out.println("Unknown product event");
    }
}
