package com.dapp.inventory.repository;

import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import com.dapp.inventory.model.InventoryItem;

public interface InventoryItemRepository extends JpaRepository<InventoryItem, Long> {
    // Get item quantity given an inventory id and a product id. If no such item
    // present then it returns empty.
    @Query("SELECT i FROM InventoryItem i WHERE i.inventory.id=:inventoryId AND i.product.id=:productId")
    Optional<Long> findItemQuantity(@Param("inventoryId") Long inventoryId, @Param("productId") Long productId);

    @Modifying
    @Query("UPDATE InventoryItem i SET i.quantity = :quantity WHERE i.inventory.id = :inventoryId AND i.product.id = :productId")
    int setItemQuantity(@Param("inventoryId") Long inventoryId, @Param("productId") Long productId, @Param("quantity") Long quantity);
}
