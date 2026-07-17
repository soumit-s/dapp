package com.dapp.inventory.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.dapp.inventory.model.Product;

public interface ProductRepository extends JpaRepository<Product, Long> {
    
}
