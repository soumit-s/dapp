package com.dapp.profileservice.common.repository;

import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;

import com.dapp.profileservice.common.entity.AdminProfile;

public interface AdminProfileRepository extends JpaRepository<AdminProfile, Long> {
    Optional<AdminProfile> findByUserId(Long userId);
}
