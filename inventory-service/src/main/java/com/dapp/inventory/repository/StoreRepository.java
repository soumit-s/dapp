package com.dapp.inventory.repository;

import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import com.dapp.inventory.model.Store;

public interface StoreRepository extends JpaRepository<Store, Long> {
    @Query("SELECT s.inventory.id FROM Store s WHERE s.id = :storeId")
    Optional<Long> findStoreInventoryId(@Param("storeId") Long storeId);
}
