package com.dapp.inventory.service;

import com.dapp.inventory.repository.InventoryItemRepository;
import java.util.Optional;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;

import com.dapp.inventory.model.InventoryItem;
import com.dapp.inventory.repository.InventoryRepository;
import com.dapp.inventory.repository.ProductRepository;
import com.dapp.inventory.repository.StoreRepository;

@Service
public class InventoryService {
    private final InventoryItemRepository inventoryItemRepository;
    private final StoreRepository storeRepository;
    private final ProductRepository productRepository;
    private final InventoryRepository inventoryRepository;

    InventoryService(InventoryItemRepository inventoryItemRepository, StoreRepository storeRepository,
            ProductRepository productRepository, InventoryRepository inventoryRepository) {
        this.inventoryItemRepository = inventoryItemRepository;
        this.inventoryRepository = inventoryRepository;
        this.productRepository = productRepository;
        this.storeRepository = storeRepository;
    }

    @Transactional(propagation = Propagation.REQUIRED)
    public void addProductToStore(long storeId, long productId, long quantity) {
        Long inventoryId = storeRepository.findStoreInventoryId(storeId)
                .orElseThrow(() -> new RuntimeException("Inventory not found exception"));

        // Get the current item quantity.
        Optional<Long> existingQuantity = inventoryItemRepository.findItemQuantity(inventoryId, productId);
        if (existingQuantity.isEmpty()) {
            // Update to item quantity to existingQuantity + quantity
            inventoryItemRepository.setItemQuantity(inventoryId, productId, existingQuantity.get() + quantity);
        } else {
            // Try to add the product to the store inventory.
            InventoryItem item = new InventoryItem();
            item.setInventory(inventoryRepository.getReferenceById(inventoryId));
            item.setProduct(productRepository.getReferenceById(productId));
            item.setQuantity(quantity);

            inventoryItemRepository.save(item);
        }
    }
}
