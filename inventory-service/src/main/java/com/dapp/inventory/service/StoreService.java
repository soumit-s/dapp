package com.dapp.inventory.service;

import org.springframework.stereotype.Service;

import com.dapp.inventory.model.Inventory;
import com.dapp.inventory.model.Store;
import com.dapp.inventory.repository.StoreRepository;
import com.dapp.inventory.schema.StoreCreatedEventDto;
import com.dapp.inventory.schema.StoreCreatedEventPayloadDto;

@Service
public class StoreService {
    private final StoreRepository storeRepository;

    public StoreService(StoreRepository storeRepository) {
        this.storeRepository = storeRepository;
    }

    public void handleCreateStoreEvent(StoreCreatedEventDto event) {
        StoreCreatedEventPayloadDto payload = event.getPayload();

        // Create the store entity.
        Store store = new Store();
        store.setId(payload.getId());
        store.setName(payload.getName());
        store.setDescription(payload.getDescription());
        
        // Create the inventory.
        Inventory inventory = new Inventory();
        // Set the inventory.
        store.setInventory(inventory);

        // Save to database
        storeRepository.save(store);
    }
}
