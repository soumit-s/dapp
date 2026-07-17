package com.dapp.inventory.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.dapp.inventory.model.Inventory;

public interface InventoryRepository extends JpaRepository<Inventory, Long>{
}
