package com.dapp.inventory.listener;

import org.springframework.kafka.annotation.KafkaHandler;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.support.Acknowledgment;
import org.springframework.stereotype.Component;

import com.dapp.inventory.schema.StoreCreatedEventDto;
import com.dapp.inventory.service.StoreService;

@Component
@KafkaListener(id="store-event-listener", groupId = "inventory-service-store-listener", topics = "outbox.store", concurrency = "4")
public class StoreEventListener {

    private final StoreService storeService;

    public StoreEventListener(StoreService storeService) {
        this.storeService = storeService;
    }

    @KafkaHandler
    public void handleStoreEvent(StoreCreatedEventDto dto, Acknowledgment ack) {
        System.out.printf("%s %s %s\n", dto.getAggregateId(), dto.getAggregateType(), dto.getPayload().getName());
        // Donot acknowledge so that we can replay through them

        // TODO: Error handling
        storeService.handleCreateStoreEvent(dto);
    }
    
    @KafkaHandler(isDefault = true)
    public void handleUnknown(Object fallback, Acknowledgment ack) {
        System.out.println("Unknown event Hua Hua He He");
        ack.acknowledge(); // Only for debugging
    }
}
